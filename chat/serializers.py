from django.contrib.auth import get_user_model
from rest_framework import serializers

from chat.models import Chat, Message

User = get_user_model()


class UserChatFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['members'] = UserChatFieldSerializer(instance=instance.members.all(), many=True).data
        return represent


class MessagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        represent = super().to_representation(instance)

        if instance.author.private_account:
            represent['is_read'] = False
        represent['author'] = instance.author.username
        represent['author_id'] = instance.author.id
        return represent


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message',)
