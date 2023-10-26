from collections.abc import Iterable
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

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

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user
class NewUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    
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
    phone_number = PhoneNumberField()
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
    phone_number = PhoneNumberField()
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