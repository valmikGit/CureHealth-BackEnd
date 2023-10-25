from rest_framework import serializers
from .models import Doctor, Patient


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = [
            "password",
            "type",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
            "is_superuser",
            "id"
        ]
        depth = 1


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = [
            "password",
            "type",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
            "is_superuser",
            "id"
        ]
        delth = 1
