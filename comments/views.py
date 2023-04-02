from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

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
        return permissions.IsAuthenticated(),


class CommentAddView(APIView):

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'msg': 'Post  not found!'}, status=404)
        data = request.data.copy()
        data['post'] = post.id
        serializer = serializers.CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response({'msg': 'success'}, status=201)

