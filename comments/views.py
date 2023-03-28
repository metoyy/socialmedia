from rest_framework import generics, permissions
from .models import *
from . import serializers
from post.permissions import IsAuthorOrAdminOrPostOwner


class CommentCreateView(generics.CreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return IsAuthorOrAdminOrPostOwner(),
        return permissions.AllowAny(),


