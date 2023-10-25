from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Doctor, Patient
from .serializers import DoctorSerializer, PatientSerializer
from rest_framework.response import Response
from django.http import HttpResponse
# Create your views here.

@api_view(['GET', 'POST'])
def patients(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = PatientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'POST'])
def doctors(request):
    if request.method == 'GET':
        patients = Doctor.objects.all()
        serializer = DoctorSerializer(patients, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = DoctorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
def home(request):
    return HttpResponse("<h1>HOME<h1>")