import pyotp
from healthcare.models import NewUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import OTP
from Synergy_Backend import settings

@api_view(['POST'])
def send_otp(request):
    if request.method == 'POST':
        email = request.data.get('email')
        print(f"Email POSTed on send otp page is : {email}")
        user = NewUser.objects.filter(email=email).first()
        
        if user:
            # Generate OTP
            otp_secret = pyotp.random_base32()
            otp = pyotp.TOTP(otp_secret)
            otp_code = otp.now()

            # Save OTP to the database
            otp_obj, created = OTP.objects.get_or_create(user=user, email=email)
            otp_obj.otp_secret = otp_secret
            otp_obj.save()

            # Send OTP via email
            subject = 'Your OTP for Login'
            message = f'Your OTP for login is: {otp_code}'
            from_email = settings.EMAIL_HOST_USER  # Update with your email
            recipient_list = [email]

            # Add Phone OTP API

            send_mail(subject, message, from_email, recipient_list)
            print("Email sent successfully.")

            # return redirect('verify-otp')
            # return redirect('http://127.0.0.1:8000/verify-auth/verify-otp/')
            return Response({
                'message' : 'User should be redirected to the verify-otp page by the front end.'
            })
        else:
            # return render(request, 'send_otp.html', {'message': 'Email not found'})
            return Response({
                'status' : 404,
                'message' : 'Email not found'
            })
    else:
        # return render(request, 'send_otp.html')
        return Response({
            'message' : 'You reached the send otp page.'
        })
    
@api_view(['POST'])
def verify_otp(request):
    if request.method == 'POST':
        email = request.data.get('email')
        print(f"Email POSTed on verify otp page is : {email}")
        otp_code = request.POST.get('otp')
        
        otp_obj = OTP.objects.filter(email=email).first()
        
        if otp_obj:
            otp = pyotp.TOTP(otp_obj.otp_secret)
            print(otp_obj.otp_secret)
            print(otp_code)
            print(otp.verify(otp_code))
            if otp.verify(otp_code):
                otp_obj.is_verified = True
                otp_obj.save()
                # user = authenticate(request, username=otp_obj.user.username, password='')
                user = authenticate(request, username=otp_obj.user.email, password='')
                if user:
                    login(request, user)
                    # return redirect('home') Replace 'home' with the URL name of your home page
                    return Response({
                        'message' : 'You are being redirected to the home page. This should be done by the frontend.'
                    })
                else:
                    # return redirect('login') Replace 'login' with the URL name of your home page
                    return Response({
                        'message' : 'You are being redirected to the login page. This should be done by the frontend.'
                    })
            else:
                # return render(request, 'verify_otp.html', {'message': 'Invalid OTP'})
                return Response({
                    'message' : 'Invalid OTP'
                })
        else:
            # return render(request, 'verify_otp.html', {'message': 'OTP not found'})
            return Response({
                'status' : 404,
                'message' : 'OTP not found. You are being redirected to the verify otp page.'
            })
    else:
        # return render(request, 'verify_otp.html')
        return Response({
            'message' : 'You reached the verify otp page'
        })
    
@api_view(['GET'])
def get_Routes(request):
    routes = [
        'send-otp/',
        'verify-otp/'
    ]
    return Response(routes)