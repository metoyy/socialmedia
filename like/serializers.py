from rest_framework import serializers

from like.models import Like


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        post = attrs['post']
        if user.likes.filter(post=post).exists():
            raise serializers.ValidationError('You already liked this post!')
        return attrs



class LikeListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ('owner', 'owner_username',)