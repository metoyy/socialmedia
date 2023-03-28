from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from comments.models import Comment
from post.models import Post
from . import serializers
from .permissions import *


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializer

    def get_permissions(self):
        # only admin or author can delete
        if self.action == 'destroy':
            return permissions.IsAuthenticated(), IsAuthorOrAdmin(),
        # only author can update
        elif self.action in ('update', 'partial_update'):
            return permissions.IsAuthenticated(), IsAuthor(),
        # listing and retrieve is allowAny, but create is for authorized only
        return permissions.IsAuthenticatedOrReadOnly(),


class PostCommentsView(APIView):
    def get(self, request, pk):
        post = Post.comments.all()
        serializer = serializers.PostSerializer(post).data
        return Response(serializer, status=200)
