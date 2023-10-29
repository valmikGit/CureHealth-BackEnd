from django.contrib import admin
from .models import NewUser, Patient, Doctor, Intermediate, Appointment
# from .models import Note
# Register your models here.
admin.site.register(NewUser)
admin.site.register(Doctor)
admin.site.register(Patient)
# admin.site.register(Note)
admin.site.register(Intermediate)
admin.site.register(Appointment)