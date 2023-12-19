from collections.abc import Iterable
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        other_fields.setdefault('is_active', True)
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        # password = make_password(password=password)
        user.set_password(password)
        user.save()
        return user
class AppointmentManager(BaseUserManager):
    def upcoming_appointments(self):
        """
        Get a queryset for all upcoming appointments.
        """
        return self.filter(meeting_Date_Time__gt=timezone.now())

    def past_appointments(self):
        """
        Get a queryset for all past appointments.
        """
        return self.filter(meeting_Date_Time__lt=timezone.now())

    def chat_appointments(self):
        """
        Get a queryset for all appointments of type CHAT.
        """
        return self.filter(meeting_Type=Appointment.MeetingType.CHAT)

    def videocall_appointments(self):
        """
        Get a queryset for all appointments of type VIDEOCALL.
        """
        return self.filter(meeting_Type=Appointment.MeetingType.VIDEOCALL)

class DoctorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return super().get_queryset(*args, **kwargs).filter(type=NewUser.Types.DOCTOR)

class PatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return super().get_queryset(*args, **kwargs).filter(type=NewUser.Types.PATIENT)

class IntermediateManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return super().get_queryset(*args, **kwargs).filter(type=NewUser.Types.INTERMEDIATE)

class NewUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = PhoneNumberField(default='1234567890')
    is_Email_Verified = models.BooleanField(default=False)
    is_Phone_Verified = models.BooleanField(default=False)
    # otp = models.CharField(max_length=6, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    
    class Types(models.TextChoices):
        DOCTOR = "DOCTOR", "Doctor"
        PATIENT = "PATIENT", "Patient"
        ADMIN = "ADMIN", "Admin"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
    
    type = models.CharField(_("Type"), max_length=50, choices=Types.choices, default=Types.ADMIN)

    objects = CustomAccountManager()

    # USERNAME_FIELD = 'username'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

class Patient(NewUser):
    class SeverityType(models.TextChoices):
        MILD = "MILD", "Mild"
        SEVERE = "SEVERE", "Severe"
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
    blood_Group = models.CharField(_("Blood group"), max_length=4, default="Blood group not mentioned.")
    ailments = models.CharField(_("Ailments"), max_length=500, default="None")
    severity = models.CharField(_("Severity"), max_length=20, choices=SeverityType.choices, default=SeverityType.MILD, blank=True, null=True)
    disease = models.TextField(verbose_name="Information about disease", null=True, blank=True)
    gender = models.CharField(_("Gender"), max_length=20, choices=Gender.choices, default=Gender.FEMALE, blank=True, null=True)
    objects = PatientManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = NewUser.Types.PATIENT
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

class Doctor(NewUser):
    class Specialization(models.TextChoices):
        CARDIOLOGIST = "CARDIOLOGIST", "Cardiologist"
        DERMATOLOGIST = "DERMATOLOGIST", "Dermatologist"
        ORTHOPEDIC = "ORTHOPEDIC", "Orthopedic"
        GYNECOLOGIST = "GYNECOLOGIST", "Gynecologist"
        NEUROLOGIST = "NEUROLOGIST", "Neurologist"
        OPHTHALMOLOGIST = "OPHTHALMOLOGIST", "Ophthalmologist"
        ENT = "ENT", "Ent"
        GASTROENTEROLOGIST = "GASTROENTEROLOGIST", "Gastroenterologist"
        PSYCHIATRIST = "PSYCHIATRIST", "Psychiatrist"
        ENDOCRINOLOGIST = "ENDOCRINOLOGIST", "Endocrinologist"

    about = models.TextField(max_length=200)
    specialization = models.CharField(_("Speciality"), max_length=20, choices=Specialization.choices)
    is_Free = models.BooleanField(_("Is the doctor free for a meeting?"))
    objects = DoctorManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = NewUser.Types.DOCTOR
            if not self.specialization:
                self.specialization = Doctor.Specialization.CARDIOLOGIST
            if not self.is_Free:
                self.is_Free = True
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
    
class Intermediate(NewUser):
    about = models.CharField(max_length=200)
    objects = IntermediateManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = NewUser.Types.INTERMEDIATE
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Intermediate person"
        verbose_name_plural = "Intermediate people"

class Appointment(models.Model):
    class MeetingType(models.TextChoices):
        CHAT = "CHAT", "Chat"
        VIDEOCALL = "VIDEOCALL", "Videocall"
    
    # intermediate = models.ForeignKey(Intermediate, on_delete=models.SET_NULL, null=True, blank=True)
    # doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    patient_ID = models.IntegerField(default=0, null=True, blank=True)
    doctor_Intermediate_ID = models.IntegerField(default=0, null=True, blank=True)
    time_difference = timedelta(hours=5, minutes=30)  # Adjust this according to your time difference
    server_time = timezone.now() - time_difference
    meeting_Date_Time = models.DateTimeField(verbose_name="Meeting Date and Time", default=server_time)
    meeting_Type = models.CharField(_("Meeting type"), max_length=50, choices=MeetingType.choices, default=MeetingType.CHAT)
    disease = models.TextField(verbose_name="Information about disease", null=True)
    video_URL = models.URLField(verbose_name="Meet link", blank=True, null=True)
    objects = AppointmentManager()

    def save(self, *args, **kwargs):
        # if self.meeting_Type == Appointment.MeetingType.VIDEOCALL and not self.video_URL:
        #     # If it's a videocall appointment and no video_URL is provided, set it based on the frontend value
        #     # Assuming you have a field in the frontend named 'frontend_video_url', replace it with your actual field
        #     video_URL = getattr(self, 'video_URL', None)
            
        #     if frontend_video_url:
        #         self.video_URL = video_URL
        #     else:
        #         # Handle the case where no video_URL is provided from the frontend
        #         raise ValueError("Video URL is required for videocall appointments.")

        # # You can add more custom logic as needed
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

# 1. Manager Classes:
# CustomAccountManager:
# Inherits from BaseUserManager, which is a Django base manager for handling user models.
# Provides methods for creating a superuser (create_superuser) and a regular user (create_user).
# The create_superuser method sets default values for is_staff, is_superuser, and is_active.
# The create_user method is responsible for creating a regular user, setting default values, normalizing the email, and saving the user with a hashed password.
# AppointmentManager:
# Inherits from BaseUserManager.
# Provides custom query methods for filtering appointments based on upcoming, past, chat, and videocall appointments.
# DoctorManager, PatientManager, IntermediateManager:
# Inherit from BaseUserManager.
# Provide custom queryset methods for filtering users based on their type attribute, which corresponds to the NewUser.Types choices.
# 2. Model Classes:
# NewUser (AbstractUser and PermissionsMixin):
# Inherits from AbstractUser and PermissionsMixin, which are Django base classes for user authentication and permissions.
# Adds custom fields such as email, phone_number, is_Email_Verified, is_Phone_Verified, id, and type.
# Defines a Types enumeration for user types (DOCTOR, PATIENT, ADMIN, INTERMEDIATE).
# Uses the CustomAccountManager as the default manager.
# Patient, Doctor, Intermediate (Inherit from NewUser):
# Inherit from NewUser and extend it with additional fields specific to each type of user.
# Each user type has its own manager (PatientManager, DoctorManager, IntermediateManager).
# Custom fields include blood_Group, ailments, severity, disease, gender for Patient; about, specialization, is_Free for Doctor; and about for Intermediate.
# Overrides the save method to set the type field based on the user type when saving.
# Appointment:
# Represents an appointment model.
# Contains fields like patient_ID, doctor_Intermediate_ID, meeting_Date_Time, meeting_Type, disease, and video_URL.
# Uses the AppointmentManager as the default manager.
# Defines a MeetingType enumeration for appointment types (CHAT, VIDEOCALL).
# Overrides the save method to add custom logic (commented out) before saving the instance.
# 3. Relationships:
# Patient, Doctor, and Intermediate models are subclasses of NewUser, which is an abstract user model.
# The Appointment model has fields referencing Patient, Doctor, and Intermediate models through ID fields (patient_ID and doctor_Intermediate_ID).
# 4. Other Points:
# The MeetingType and Types choices are defined as enumerations using models.TextChoices.
# The PhoneNumberField from phonenumber_field is used for the phone_number field in the NewUser model.
# Custom logic is added in the save methods of models for additional functionalities.
# In summary, this code defines a flexible user model hierarchy with different types of users (Patient, Doctor, Intermediate), each with its own set of attributes. The Appointment model handles appointments between users, and the manager classes provide custom queries and filtering for these models. The code follows best practices for Django models and managers, allowing for extensibility and customization.
    