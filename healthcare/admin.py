from django.contrib import admin
from .models import NewUser, Patient, Doctor
# Register your models here.
admin.site.register(NewUser)
admin.site.register(Doctor)
admin.site.register(Patient)