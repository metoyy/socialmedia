from abc import ABC

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from account.models import FriendRequest
from .tasks import *
from post.serializers import PostSerializer

User = get_user_model()


class FriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('friends',)

    def to_representation(self, instance):
        return {'friends': FriendSerializer(instance.related_friends.all(), many=True).data}


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'activation_code', 'password_reset_code', 'user_permissions', 'friends',)

    def to_representation(self, instance):
        if not instance.private_account:
            represent = super().to_representation(instance)
            return represent
        else:
            represent = super().to_representation(instance)
            represent.pop('last_login')
            represent.pop('date_joined')
            represent.pop('first_name')
            represent.pop('last_name')
            represent.pop('profile_quote')
            represent.pop('groups')
            return represent


class UserModifySerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture', 'profile_quote',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'activation_code', 'password_reset_code', 'user_permissions',
                   'friends', 'is_staff', 'is_active', 'balance', 'recommendations')

    def validate(self, attrs):
        return super().validate(attrs)

    def to_representation(self, instance):
        print(instance)
        print(self.context)
        represent = super().to_representation(instance)
        represent['friends'] = FriendSerializer(instance.related_friends.all(), many=True).data
        represent['posts'] = PostSerializer(instance=instance.posts.all(), many=True).data
        return represent


class UserSelfSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'activation_code', 'password_reset_code', 'user_permissions',)

    def validate(self, attrs):
        return super().validate(attrs)

    def to_representation(self, instance):
        print(instance)
        print(self.context)
        represent = super().to_representation(instance)
        represent['friends'] = FriendSerializer(instance.related_friends.all(), many=True).data
        represent['posts'] = PostSerializer(instance=instance.posts.all(), many=True).data
        return represent


class UserPrivateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'activation_code', 'password_reset_code', 'user_permissions',
                   'friends', 'is_staff', 'is_active', 'balance')

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent.pop('last_login')
        represent.pop('date_joined')
        represent.pop('first_name')
        represent.pop('last_name')
        represent.pop('profile_quote')
        represent.pop('groups')
        return represent


class UserListSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'activation_code', 'password_reset_code', 'user_permissions',
                   'friends', 'is_staff', 'is_active', 'recommendations', 'balance',)

    def validate(self, attrs):
        return super().validate(attrs)

    def to_representation(self, instance):
        if not instance.private_account:
            represent = super().to_representation(instance)
            return represent
        else:
            represent = super().to_representation(instance)
            represent.pop('last_login')
            represent.pop('date_joined')
            represent.pop('first_name')
            represent.pop('last_name')
            represent.pop('profile_quote')
            represent.pop('groups')
            return represent


class UserPrivateOwnerSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'activation_code', 'password_reset_code', 'user_permissions',
                   'friends', 'is_staff', 'is_active')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=30, required=True,
                                     write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=30, required=True,
                                      write_only=True)
    username = serializers.CharField(min_length=5, max_length=35, required=True)

    class Meta:
        model = User
        fields = ('email',
                  'password',
                  'password2',
                  'first_name',
                  'last_name',
                  'username',
                  'profile_picture',
                  'profile_quote',
                  )

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        username = attrs['username']
        if password != password2:
            raise serializers.ValidationError('Passwords didn\'t match!')
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                'Password field must contain alpha and numeric symbols!'
            )
        if len(password) < 8:
            raise serializers.ValidationError(
                'Password field must be more than 8 symbols!'
            )
        try:
            users = User.objects.get(username=username)
            raise serializers.ValidationError('User with that username already exists!')
        except User.DoesNotExist:
            return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=255)
    default_error_messages = {
        'bad_code': _('Code is expired or invalid!')
    }

    def validate(self, attrs):
        self.code = attrs['code']
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.get(activation_code=self.code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            send_welcome.delay(user.email)
        except User.DoesNotExist:
            self.fail('bad_code')


class PasswordResetSerializer(serializers.Serializer):
    password_reset_code = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=30, min_length=8, write_only=True)
    password2 = serializers.CharField(required=True, max_length=30, min_length=8, write_only=True)
    default_error_messages = {
        'bad_code': _('Code is expired or invalid!')
    }

    def validate(self, attrs):
        self.password_reset_code = attrs['password_reset_code']
        password2 = attrs.pop('password2')
        password = attrs['password']
        if password2 != password:
            raise serializers.ValidationError('Passwords didn\'t match!')
        if password == User.password:
            raise serializers.ValidationError('Password cant be previous!')
        user = User.objects.get(password_reset_code=attrs['password_reset_code'])
        user.set_password(password)
        send_changed_pw_notification.delay(user.email,)
        user.save()
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.get(password_reset_code=self.password_reset_code)
            user.password_reset_code = None
            user.save()
        except User.DoesNotExist:
            self.fail('bad_code')


class FriendRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'


class FriendReqInSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        exclude = ('to_user',)

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        user = User.objects.get(id=represent['from_user'])
        req_id = represent.pop('id')
        user_id = represent.pop('from_user')
        represent['user_id'] = user_id
        represent['request_id'] = req_id
        represent['email'] = user.email
        represent['username'] = user.username
        return represent


class FriendReqOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        exclude = ('from_user',)

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        user = User.objects.get(id=represent['to_user'])
        req_id = represent.pop('id')
        user_id = represent.pop('to_user')
        represent['user_id'] = user_id
        represent['request_id'] = req_id
        represent['email'] = user.email
        represent['username'] = user.username
        return represent


class FriendHandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('active',)


class TopUpBalanceSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(required=True, decimal_places=2, max_digits=100)

    class Meta:
        model = User
        fields = ('balance',)

    def validate(self, attrs):
        if attrs['balance'] > 0:
            self.top_up = attrs['balance']
        else:
            raise serializers.ValidationError('Balance must be positive!')
        return attrs

    def save(self, **kwargs):
        user = kwargs['user']
        user = User.objects.get(id=user.id)
        user.balance += self.top_up
        user.save()


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('balance',)

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        repre = dict()
        repre['balance'] = represent['balance']
        return repre
