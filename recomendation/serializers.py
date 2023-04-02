from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.serializers import UserListSerializer
from post.models import Post
from post.serializers import PostRecommendSerializer
from recomendation.models import Recommendation

User = get_user_model()


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ('members', 'posts')

    def validate(self, attrs):
        super().validate(attrs)
        print(attrs)
        return attrs

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent.pop('members')
        represent.pop('posts')
        recommend = Recommendation.objects.get(author=instance.author)
        members = recommend.members
        posts = recommend.posts.order_by('created_at',).reverse()
        represent['friend_recommendations'] = UserListSerializer(instance=members, many=True).data
        represent['all_posts'] = PostRecommendSerializer(instance=posts, many=True).data
        return represent
