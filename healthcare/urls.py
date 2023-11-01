from django.contrib import admin
from django.urls import path
from healthcare import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

urlpatterns = [
    path('', view=views.home),
    path('doctors/', view=views.doctors, name="All Doctors"),
    path('patients/', view=views.patients, name="All patients"),
    path('allusers/', view=views.new_Users, name="Users list"),
    path('intermediates/', view=views.intermediates, name="Intermediate Assistance People's list")
    # path('doctors/', view=views.get_doctors_by_speciality),
    # path('verify-otp/', view=views.verify_OTP),
]


