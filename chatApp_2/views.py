from django.shortcuts import render
from django.db.models import Subquery, OuterRef, Q
from rest_framework import generics, status
from chatApp_2.models import ChatMessage
from chatApp_2.serializers import ChatMessageSerializer
from healthcare.models import NewUser
from healthcare.serializers import NewUserSerializer
from django.http import JsonResponse
from rest_framework.response import Response

class MyInbox(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')

        messages = ChatMessage.objects.filter(
            id__in=Subquery(
                NewUser.objects.filter(
                    Q(sender__receiver=user_id) |
                    Q(receiver__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), receiver=user_id) |
                            Q(receiver=OuterRef('id'), sender=user_id)
                        ).order_by("-id")[:1].values_list("id", flat=True)
                    )
                ).values_list("last_msg", flat=True).order_by("-id")
            )
        ).order_by("-id")

        return messages

def chat_2_Home(request):
    return JsonResponse({
        'status' : 200,
        'message' : 'You reached the home page of the chatApp_2'
    })

class GetMessages(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        sender_id = self.request.query_params.get('sender_id')
        receiver_id = self.request.query_params.get('receiver_id')

        messages = ChatMessage.objects.filter(
            sender_id=sender_id,
            receiver_id=receiver_id
        )

        return messages

class SendMessages(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer

class SearchUser(generics.ListAPIView):
    serializer_class = NewUserSerializer
    queryset = NewUser.objects.all()

    def list(self, request, *args, **kwargs):
        username = self.request.query_params.get('username')
        logged_in_user = self.request.user
        users = NewUser.objects.filter(
            Q(user__username__icontains=username) |
            Q(full_name__icontains=username) |
            Q(user__email__icontains=username)
        )

        if not users.exists():
            return Response(
                {
                    "detail" : "No users found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
