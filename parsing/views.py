from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from account import serializers
from chat.models import Message
from post.models import Post
from post.serializers import PostSerializer

from datetime import datetime

# Create your views here.


User = get_user_model()


class UserListView(APIView):
    permission_classes = permissions.AllowAny,

    def get(self, request):
        user = User.objects.all()
        serializer = serializers.UserListSerializer(instance=user, many=True)
        return Response(serializer.data, status=200)


class PostListView(APIView):
    permission_classes = permissions.AllowAny,

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(instance=posts, many=True)
        return Response(serializer.data, status=200)


class OverallStatsView(APIView):
    permission_classes = permissions.AllowAny,

    def get(self, request):
        posts = Post.objects.all()
        users = User.objects.all()
        msgs = Message.objects.all()
        respo = {'posts_count': posts.count(), 'users_count': users.count(), 'messages_count': msgs.count(),
                 'request_date': datetime.now().strftime('%d  %h  %Y || %H:%M:%S')}
        return Response(respo, status=200)
