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
            "id"
        ]
        extra_kwargs = {'password' : {'write_only' : True}}
        depth = 1
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        return CustomAccountManager().create_user(password=password, **validated_data)

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
            "id"
        ]
        extra_kwargs = {'password' : {'write_only' : True}}
        depth = 1

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        return CustomAccountManager().create_user(password=password, **validated_data)

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
            "id"
        ]
        extra_kwargs = {'password' : {'write_only' : True}}
        depth = 1

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        return CustomAccountManager().create_user(password=password, **validated_data)

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
            "id"
        ]
        extra_kwargs = {'password' : {'write_only' : True}}
        depth = 1

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        return CustomAccountManager().create_user(password=password, **validated_data)

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        depth = 1
