from abc import ABC

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


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
        user.save()
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.get(password_reset_code=self.password_reset_code)
            user.password_reset_code = ''
            user.save()
        except User.DoesNotExist:
            self.fail('bad_code')

