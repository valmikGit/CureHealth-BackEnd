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
            patients = NewUser.objects.filter(id=patient_Id)
            if(not patients.exists()):
                return Response({
                    'message' : 'User with this ID does not exist'
                })
            if(patients.first().type != NewUser.Types.PATIENT):
                return Response({
                    'message' : 'User exists but is not of type Patient.'
                })
            particular_Patient = Patient.objects.filter(id=patient_Id).first()
            serializer = NewUserSerializer(patients, many=True)
            return Response({
                'blood_Group' : particular_Patient.blood_Group,
                'gender' : particular_Patient.gender,
                'disease' : particular_Patient.disease,
                'patient_As_NewUser' : serializer.data
            })
        else: 
            patients = Patient.objects.all()
            # serializer = PatientSerializer(patients, many=True)
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
                'message' : 'Patient added to database, GET to check whether database was updated.',
                'id' : serializer.data['id']
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
        # speciality = request.query_params.get('speciality', None)
        doctor_Id = request.GET.get('id', None)
        specialization = request.GET.get('specialization', None)
        if doctor_Id is not None:
            doctors = NewUser.objects.filter(id=doctor_Id)
            if(not doctors.exists()):
                return Response({
                    'message' : 'User with this ID does not exist.'
                })
            if(doctors.first().type != NewUser.Types.DOCTOR):
                return Response({
                    'message' : 'User exists but is not of Doctor type.'
                })
            particular_Doctor = Doctor.objects.filter(id=doctor_Id).first()
            serializer = NewUserSerializer(doctors, many=True)
            # return Response(serializer.data)
            return Response({
                'about' : particular_Doctor.about,
                'specialization' : particular_Doctor.specialization,
                'is_Free' : particular_Doctor.is_Free,
                'doctor_As_NewUser' : serializer.data
            })
        elif specialization is not None:
            doctors = Doctor.objects.filter(specialization=specialization)
            doctors_Free = doctors.filter(is_Free=True)
            if(not doctors_Free.exists()):
                return Response({
                    'message': f"{specialization}s are not free right now."
                })
            serializer = DoctorSerializer(doctors_Free, many=True)
            return Response(serializer.data)
        else:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
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
                'message' : 'Doctor added to database, GET to check whether database was updated.',
                'id' : serializer.data['id']
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

    # elif request.method == 'PUT':
    #     data = request.data

    #     # Fetch the instance to update using the ID provided in the data
    #     try:
    #         doctor_instance = Doctor.objects.get(id=data['id'])
    #     except Doctor.DoesNotExist:
    #         return Response(
    #             {"error": "Doctor with this ID does not exist"}
    #         )

    #     # Pass the instance to the serializer
    #     serializer = DoctorSerializer(instance=doctor_instance, data=data)

    #     # Validate and save the updated data
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)

    #     return Response(serializer.errors)
    
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
            if(not new_User.exists()):
                return Response({
                    'message' : 'User with this ID does not exist.'
                })
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
        # username = request.query_params.get('username', None)
        intermediate_Id = request.GET.get('id', None)
        if intermediate_Id is not None:
            intermediate_People = NewUser.objects.filter(id=intermediate_Id)
            if(not intermediate_People.exists()):
                return Response({
                    'message' : 'User with this ID does not exist.'
                })
            if(intermediate_People.first().type != NewUser.Types.INTERMEDIATE):
                return Response({
                    'message' : 'User exists but is not of Intermediate type.'
                })
            serializer = NewUserSerializer(intermediate_People, many=True)
            return Response(serializer.data)
        else:
            intermediate_People = Intermediate.objects.all()
            serializer = IntermediateSerializer(intermediate_People, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
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
                'message' : 'Intermediate added to database, GET to check whether database was updated.',
                'id' : serializer.data['id']
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
        # appointment_Filter = request.query_params.get('filter', None)
        appointment_Filter = request.GET.get('filter', None)
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
            doctor = Doctor.objects.filter(id=serializer.data['doctor_Intermediate_ID'])
            doctor.is_Free = False
            return Response({
                'status' : 200,
                'message' : 'Appointment added to database, GET to check whether database was updated.',
                'id' : serializer.data['id']
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

 