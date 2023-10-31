from healthcare.serializers import NewUserSerializer
from chatApp_2.models import ChatMessage
from rest_framework import serializers

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            'sender',
            'receiver',
            'user',
            'message',
            'is_read',
            'date',
            'id'
        ]