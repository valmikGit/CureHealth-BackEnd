from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Doctor, Patient, NewUser, Intermediate, Appointment
from .serializers import DoctorSerializer, PatientSerializer, NewUserSerializer, AppointmentSerializer, IntermediateSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
# from healthcare.helpers import send_otp_to_mobile
from django.http import JsonResponse
# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def patients(request):
    if request.method == 'GET':
        # severity = request.query_params.get('severity', None)
        patient_Id = request.GET.get('id', None)
        if patient_Id is not None:
            patients = Patient.objects.filter(id=patient_Id)
            # serializer = PatientSerializer(patients, many=True)
            serializer = PatientSerializer(patients)
            return Response(serializer.data)
        else:
            print("id is none.") 
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
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response({
                'status' : 200,
                'message' : 'User added to database, GET to check whether database was updated.'
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
                # return Response(serializer.errors)
                return Response({
                    'status' : 403,
                    'errors' : serializer.errors
                })
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
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
    user_id = request.query_params.get('id', None)
    if user_id is not None:
        try:
            new_User = NewUser.objects.filter(id=user_id)
            serializer = NewUserSerializer(new_User)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'status' : 404,
                'message' : f"Error : {e}"
            })
    else:
        if request.method == 'GET':
            patients = NewUser.objects.all()
            serializer = NewUserSerializer(patients, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            data = request.data
            serializer = NewUserSerializer(data=data)
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
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
            
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def intermediates(request):
    if request.method == 'GET':
        username = request.query_params.get('username', None)
        if username is not None:
            intermediate_People = Intermediate.objects.filter(username=username)
            serializer = IntermediateSerializer(intermediate_People, many=True)
            return Response(serializer.data)
        else:
            intermediate_People = Intermediate.objects.all()
            serializer = IntermediateSerializer(intermediate_People, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        try:
            serializer = IntermediateSerializer(data=data)
            if not serializer.is_valid():
                # return Response(serializer.errors)
                return Response({
                    'status' : 403,
                    'errors' : serializer.errors
                })
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
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
        serializer = IntermediateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = Intermediate.objects.get(id=data['id'])
        serializer = IntermediateSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        data = request.data
        try:
            obj = Intermediate.objects.get(id=data['id'])
            name = obj.username
            obj.delete()
            return Response({'message' : f"{name} deleted successfully."})
        except Exception as e:
            return Response({'message' : f"Error is {e}"})
        
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def appointments_View(request):
    if request.method == 'GET':
        # appointment_Id = request.query_params.get('id', None)
        # if appointment_Id is not None:
        #     appointments = Appointment.objects.filter(id=appointment_Id)
        #     serializer = AppointmentSerializer(appointments, many=True)
        #     return Response(serializer.data)
        # else:   
        #     patients = Appointment.objects.all()
        #     serializer = AppointmentSerializer(patients, many=True)
        #     return Response(serializer.data)
        appointment_Filter = request.query_params.get('filter', None)
        if appointment_Filter is not None:
            if appointment_Filter == "upcoming":
                appointments = Appointment.objects.upcoming_appointments()
                serializer = AppointmentSerializer(appointments, many=True)
                return Response(serializer.data)
            elif appointment_Filter == "past":
                appointments = Appointment.objects.past_appointments()
                serializer = AppointmentSerializer(appointments, many=True)
                return Response(serializer.data)
            elif appointment_Filter == "chat":
                appointments = Appointment.objects.chat_appointments()
                serializer = AppointmentSerializer(appointments, many=True)
                return Response(serializer.data)
            elif appointment_Filter == "videocall":
                appointments = Appointment.objects.videocall_appointments()
                serializer = AppointmentSerializer(appointments, many=True)
                return Response(serializer.data)
        else:
            appointments = Appointment.objects.all()
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        try:
            serializer = AppointmentSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'status' : 403,
                    'errors' : serializer.errors
                })
            serializer.save()
            return Response({
                'status' : 200,
                'message' : 'Appointment added to database, GET to check whether database was updated.'
            })
        except Exception as e:
            print(e)
            return Response({
                'status' : 200,
                'error' : 'something went wrong'
            })
    
    elif request.method == 'PUT':
        data = request.data
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = Appointment.objects.get(id=data['id'])
        serializer = AppointmentSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        data = request.data
        try:
            obj = Appointment.objects.get(id=data['id'])
            name = obj.username
            obj.delete()
            return Response({'message' : f"{name} deleted successfully."})
        except Exception as e:
            return Response({'message' : f"Error is {e}"})
    
@api_view(['GET'])
def home(request):
    routes = [
        'doctors/',
        'patients/',
        'verify-otp/',
        'allusers/',
        'intermediates/',
        'appointments/'
    ]
    return Response(routes)

 