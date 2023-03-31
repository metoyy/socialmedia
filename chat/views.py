from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render, redirect
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from chat.models import Chat
from .serializers import *

# Create your views here.

User = get_user_model()


class DialogsView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        serializer = ChatListSerializer(instance=chats, many=True).data
        return Response(serializer, status=200) if serializer \
            else Response({'msg': 'No dialogs!'}, status=200)


class MessagesView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.messages.filter(is_read=False).exclude(author=request.user).update(is_read=True)
            else:
                return Response({'msg': 'You are not a member of this chat!'}, status=400)
        except Chat.DoesNotExist:
            return Response({'msg': 'Chat not found!'}, status=404)
        messages = chat.messages.all()
        serializer = MessagesListSerializer(instance=messages, many=True).data
        return Response(serializer, status=200)

    def post(self, request, chat_id):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(chat=Chat.objects.get(id=chat_id), author=request.user)
        return redirect(f'/api/chats/dialogs/{chat_id}/')


class CreateDialogView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id],
                                    type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            new_user = User.objects.get(id=user_id)
            chat.members.add(request.user)
            chat.members.add(new_user)
        else:
            chat = chats.first()
        return redirect(f'/api/chats/dialogs/{chat.id}/',)
