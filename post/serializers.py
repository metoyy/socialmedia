from rest_framework import serializers

from comments.serializers import CommentSerializer
from .models import *
from like.serializers import LikeListSerializer


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'preview', 'owner_username', 'comments')

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['comments'] = CommentSerializer(instance=instance.comments.all(), many=True).data
        return represent


class PostRecommendSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'preview', 'owner_username', 'comments')

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['comments'] = instance.comments.all().count()
        return represent


class PostCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('comments',)

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['comments'] = CommentSerializer(instance=instance.comments.all(), many=True).data
        return represent


class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'preview', 'owner_username')

    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()

    @staticmethod
    def is_favorite(post, user):
        return user.favorite_posts.filter(id=post.id).exists()

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['likes_count'] = instance.likes.count()
        user = self.context['request'].user
        if user.is_authenticated:
            represent['is_liked'] = self.is_liked(instance, user)
            represent['is_favorite'] = self.is_favorite(instance, user)
        return represent


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    images = PostImageSerializer(many=True)

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
        user = self.context['request'].user
        if user.is_authenticated:
            represent['is_liked'] = self.is_liked(instance, user)
            represent['is_favorite'] = self.is_favorite(instance, user)
        return represent


class PostCreateSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'preview', 'images',)

    def create(self, validated_data):
        request = self.context['request']
        images_data = request.FILES.getlist('images')
        post = Post.objects.create(**validated_data)
        for image in images_data:
            PostImages.objects.create(image=image, post=post)
        return post


class PostSearchListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'preview', 'owner_username')

    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()

    @staticmethod
    def is_favorite(post, user):
        return user.favorite_posts.filter(id=post.id).exists()

    def to_representation(self, instance):
        represent = dict()
        # represent = super().to_representation(instance)
        user = self.context
        represent['post_id'] = instance.id
        represent['post_title'] = instance.title
        represent['post_owner'] = instance.owner.id
        represent['post_owner_username'] = instance.owner.username
        represent['preview'] = instance.preview.url
        represent['likes_count'] = instance.likes.count()
        if user.is_authenticated:
            represent['is_liked'] = self.is_liked(instance, user)
            represent['is_favorite'] = self.is_favorite(instance, user)
        return represent
