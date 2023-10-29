from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Doctor, Patient, NewUser
from .serializers import DoctorSerializer, PatientSerializer, NewUserSerializer, AppointmentSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from healthcare.helpers import send_otp_to_mobile
from django.http import JsonResponse
# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def patients(request):
    if request.method == 'GET':
        severity = request.query_params.get('severity')
        if severity is not None:
            patients = Patient.objects.filter(severity=severity)
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data)
        else:   
            patients = Patient.objects.all()
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        try:
            serializer = PatientSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'status' : 403,
                    'errors' : serializer.errors
                })
            serializer.save()
            return Response({
                'status' : 200,
                'message' : 'An OTP was sent to your number and email was sent for verification'
            })
        except Exception as e:
            print(e)
            return Response({
                'status' : 200,
                'error' : 'something went wrong'
            })
    
    elif request.method == 'PUT':
        data = request.data
        serializer = PatientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = Patient.objects.get(id=data['id'])
        serializer = PatientSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        data = request.data
        try:
            obj = Patient.objects.get(id=data['id'])
            name = obj.username
            obj.delete()
            return Response({'message' : f"{name} deleted successfully."})
        except Exception as e:
            return Response({'message' : f"Error is {e}"})


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def doctors(request):
    if request.method == 'GET':
        speciality = request.query_params.get('speciality', None)
        if speciality is not None:
            doctors = Doctor.objects.filter(speciality=speciality)
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)
        else:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        try:
            serializer = DoctorSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'status' : 403,
                    'errors' : serializer.errors
                })
            serializer.save()
            return Response({
                'status' : 200,
                'message' : 'An OTP was sent to your number and email was sent for verification'
            })
        except Exception as e:
            print(e)
            return Response({
                'status' : 200,
                'error' : 'something went wrong'
            })
    
    elif request.method == 'PUT':
        data = request.data
        serializer = DoctorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = Doctor.objects.get(id=data['id'])
        serializer = DoctorSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        data = request.data
        try:
            obj = Doctor.objects.get(id=data['id'])
            name = obj.username
            obj.delete()
            return Response({'message' : f"{name} deleted successfully."})
        except Exception as e:
            return Response({'message' : f"Error is {e}"})
        
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def new_Users(request):
    if request.method == 'GET':
        patients = NewUser.objects.all()
        serializer = NewUserSerializer(patients, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = NewUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = NewUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = NewUser.objects.get(id=data['id'])
        serializer = NewUserSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        data = request.data
        try:
            obj = NewUser.objects.get(id=data['id'])
            name = obj.username
            obj.delete()
            return Response({'message' : f"{name} deleted successfully."})
        except Exception as e:
            return Response({'message' : f"Error is {e}"})
    
@api_view(['GET'])
def home(request):
    routes = [
        'data/doctors/',
        'data/patients/',
        'data/verify-otp/',
        'allusers/'
    ]
    return Response(routes)

@api_view(['POST', 'PATCH'])
def verify_OTP(request):
    if request.method == 'POST':
        try:
            data = request.data
            user_Obj = NewUser.objects.get(phone_number=data['phone_number'])
            otp = data.get('otp')

            if user_Obj.otp == otp:
                user_Obj.is_Phone_Verified = True
                user_Obj.save()
                return Response({
                    'status' : 200,
                    'message' : 'Your OTP is verified.'
                })

            return Response({
                'status' : 403,
                'message' : 'Your OTP is wrong'
            })
        except Exception as e:
            print(e)
        return Response({
            'status' : 404,
            'messsage' : 'Something went wrong'
        })
    
    elif request.method == 'PATCH':
        try:
            data = request.data
            user_Obj = NewUser.objects.filter(phone_number=data['phone_number'])
            if not user_Obj.exists():
                return Response({
                    'status' : 404,
                    'error' : 'No user found!!'
                })
            
            status, time_Left = send_otp_to_mobile(mobile=data.get('phone_number'), user_Obj=user_Obj[0])

            if status:
                return Response({
                    'status' : 200,
                    'message' : 'New OTP sent'
                })
            return Response({
                'status' : 404,
                'message' : f"Try after {time_Left} seconds"
            })
        
        except Exception as e:
            print(e)
        
        return Response({
            'status' : 404,
            'message' : 'Something went wrong!'
        })

@api_view(['GET'])
def get_doctors_by_speciality(request):
    if request.method == 'GET':
        speciality = request.query_params.get('speciality', None)
        if speciality is not None:
            doctors = Doctor.objects.filter(speciality=speciality)
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({
                'status' : 400,
                'message' : 'Speciality not provided'
            })
        
@api_view(['GET'])
def get_patients_by_severity(request):
    if request.method == "GET":
        severity = request.query_params.get('severity', None)
        if severity is not None:
            patients = Patient.objects.filter(severity=severity)
            serializer = AppointmentSerializer(patients, many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({
                'status' : 400
            })

 