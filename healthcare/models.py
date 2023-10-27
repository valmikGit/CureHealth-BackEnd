from collections.abc import Iterable
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import uuid
from django.conf import settings
from healthcare.helpers import send_otp_to_mobile

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
        user.set_password(password)
        user.save(using=self._db)
        send_otp_to_mobile(mobile=user.phone_number, user_Obj=user)
        return user
class NewUser(AbstractUser, PermissionsMixin):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = PhoneNumberField(default='123456789')
    is_Email_Verified = models.BooleanField(default=False)
    is_Phone_Verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    
    class Types(models.TextChoices):
        DOCTOR = "DOCTOR", "Doctor"
        PATIENT = "PATIENT", "Patient"
        ADMIN = "ADMIN", "Admin"
    type = models.CharField(_("Type"), max_length=50, choices=Types.choices, default=Types.ADMIN)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
    
class DoctorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return super().get_queryset(*args, **kwargs).filter(type=NewUser.Types.DOCTOR)

class PatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return super().get_queryset(*args, **kwargs).filter(type=NewUser.Types.PATIENT)

class Patient(NewUser):
    blood_Group = models.CharField(_("Blood group"), max_length=4, default="Blood group not mentioned.")
    ailments = models.CharField(_("Ailments"), max_length=500, default="None")
    objects = PatientManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = NewUser.Types.PATIENT
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
class Doctor(NewUser):
    about = models.CharField(max_length=200)
    speciality = models.CharField(max_length=100)
    objects = DoctorManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = NewUser.Types.DOCTOR
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

class Note(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True)
    body = models.TextField()

    def __str__(self) -> str:
        return (f"{self.user.username}'s note")
    
@receiver(post_save, sender=NewUser)
def send_Email_Token(sender, instance, created, **kwargs):
    if created:
        try:
            subject = "Your email needs to be verified."
            message = f"Hello, click on the link to verify your email: http://127.0.0.1:8000/{uuid.uuid4()}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [instance.email]
            send_mail(subject=subject, message=message, from_email=email_from, recipient_list=recipient_list)
        except Exception as e:
            print(e)