from healthcare.models import NewUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail, mail_admins
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from Synergy_Backend import settings
import secrets
import string

def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

@api_view(['POST'])
def send_Email(request):
    if request.method == "POST":
        subject_Type = request.data.get('subject_Type')
        if subject_Type == 1: # FEEDBACK EMAIL
            email = request.data.get('email')
            subject = request.data.get('subject')
            message = f"The feedback was sent from {email}.\nFeedback:\n{request.data.get('message')}"
            mail_admins(subject=subject, message=message, fail_silently=False)
            return Response({
                'message' : 'An email was sent to the admins. Thanks for sharing your feedback.'
            })

        if subject_Type == 2: # ROOM ID AND ROOM LINK SEND TO PATIENT
            email = request.data.get('email')
            video_Call_Link = request.data.get('VC_Link')
            room_ID = request.data.get('room_ID')
            message = f"Please click on this link to join the video call : {video_Call_Link}\nEnter the given Room ID : {room_ID}"
            subject = "Appointment with doctor"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
            return Response({
                'alert' : 'A mail has been sent to you for the video calling details. Please check your email.'
            })
        
        if subject_Type == 3: # ROOM ID AND ROOM LINK SEND TO DOCTOR
            email = request.data.get('email')
            video_Call_Link = request.data.get('VC_Link')
            room_ID = request.data.get('room_ID')
            message = f"Please click on the link to join the video call : {video_Call_Link}\nEnter the given ROOM ID : {room_ID}"
            subject = "Appointment with patient"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
            return Response({
                'alert' : 'An email has been sent to the doctor. The doctor will join soon.'
            })

@api_view(['GET'])
def get_Routes(request):
    routes = [
        'send-email/'
    ]
    return Response(routes)