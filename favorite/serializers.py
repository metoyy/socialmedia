from rest_framework import serializers

from comments.serializers import CommentSerializer
from like.serializers import LikeListSerializer
from post.models import Post


class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('favorite',)

    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()

    @staticmethod
    def is_favorite(post, user):
        return user.favorite_posts.filter(id=post.id).exists()

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['comments_count'] = instance.comments.count()
        represent['comments'] = CommentSerializer(instance=instance.comments.all(), many=True).data
        represent['likes_count'] = instance.likes.count()
        represent['likes'] = LikeListSerializer(instance=instance.likes.all(), many=True).data
        user = self.context
        if user.is_authenticated:
            represent['is_liked'] = self.is_liked(instance, user)
            represent['is_favorite'] = self.is_favorite(instance, user)
        return represent
