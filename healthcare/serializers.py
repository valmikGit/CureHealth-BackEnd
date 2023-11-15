from rest_framework import serializers
from .models import Doctor, Patient, NewUser, Appointment, Intermediate, CustomAccountManager

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = [
            # "password",
            "type",
            "is_staff",
            # "is_active",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
            # "is_superuser",
            # "id"
        ]
        depth = 1

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = [
            # "password",
            "type",
            "is_staff",
            # "is_active",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
            # "is_superuser",
            # "id"
        ]
        depth = 1

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        exclude = [
            # "password",
            "is_staff",
            # "is_active",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
            # "is_superuser",
            # "id"
        ]
        depth = 1

class IntermediateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intermediate
        exclude = [
            # "password",
            "type",
            "is_staff",
            # "is_active",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
            # "is_superuser",
            # "id"
        ]
        depth = 1

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        depth = 1
