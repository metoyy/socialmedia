from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import UserListSerializer
from post.models import Post
from post.serializers import PostSearchListSerializer


User = get_user_model()
# Create your views here.


class PostSearchView(APIView):
    def get(self, request):
        search_query = request.GET['search']
        post = Post.objects.filter(title__icontains=search_query)
        serializer = PostSearchListSerializer(instance=post, many=True, context=request.user).data
        return Response(serializer, status=200) if serializer \
            else Response({'msg': 'posts not found'}, status=204)

    def post(self, request):
        search_query = request.GET['search']
        # print(search_query)
        post = Post.objects.filter(title__icontains=search_query)
        # print(post)
        serializer = PostSearchListSerializer(instance=post, many=True, context=request.user).data
        return Response(serializer, status=200) if serializer \
            else Response({'msg': 'posts not found'}, status=204)


class UserSearchView(APIView):
    def get(self, request):
        search_query = request.GET['search']
        user = User.objects.filter(username__icontains=search_query)
        serializer = UserListSerializer(instance=user, many=True).data
        return Response(serializer, status=200) if serializer \
            else Response({'msg': 'users not found'}, status=204)
