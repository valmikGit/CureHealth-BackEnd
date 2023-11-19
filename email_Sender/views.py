from healthcare.models import NewUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from Synergy_Backend import settings

@api_view(['POST'])
def send_Email(request):
    if request.method == "POST":
        subject_Type = request.data.get('subject_Type')
        if subject_Type == 1:
            email = request.data.get('email')
            print(f"Email POSTed on feedback page is {email}")
            subject = request.data.get('subject')
            message = request.data.get('message')
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return Response({
                'message' : 'Feedback email sent to admin successfully'
            })
        if subject_Type == 2:
            email = request.data.get('email')
            print(f"Email POSTed on reminder page is {email}")
            subject = request.data.get('subject')
            message = request.data.get('message')
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
            return Response({
                'message' : 'Reminder email sent to patient successfully'
            })

@api_view(['GET'])
def get_Routes(request):
    routes = [
        'send-email/'
    ]
    return Response(routes)