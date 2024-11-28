from django.contrib import admin
from django.urls import path
from healthcare import views
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
#     TokenObtainPairView
# )

urlpatterns = [
    path('', view=views.home),
    path('doctors/', view=views.doctors, name='doctors'),
    path('patients/', view=views.patients, name='patients'),
    path('allusers/', view=views.new_Users, name='users'),
    path('intermediates/', view=views.intermediates, name='intermediates'),
    path('appointments/', view=views.appointments_View, name='appointments')
    # path('doctors/', view=views.get_doctors_by_speciality),
    # path('verify-otp/', view=views.verify_OTP),
]


