from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from like import serializers
from like.models import Like
from post.models import Post
from post.permissions import IsAuthor


class LikeCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'msg': 'Post not found!'}, status=404)
        data = request.data.copy()
        data['post'] = post.id
        serializer = serializers.LikeSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response({'msg': 'success'}, status=200)


class LikeDeleteView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAuthor,)
    
    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'msg': 'Post not found!'}, status=404)
        try:
            user_like = post.likes.get(owner=request.user)
        except Like.DoesNotExist:
            return Response({'msg': 'Error!'}, status=400)
        user_like.delete()
        return Response({'msg': 'like deleted!'}, status=204)
        
