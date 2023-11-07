from django.contrib import admin
from django.urls import path
from healthcare import views
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
#     TokenObtainPairView
# )

urlpatterns = [
    path('', view=views.home),
    path('doctors/', view=views.doctors),
    path('patients/', view=views.patients),
    path('allusers/', view=views.new_Users),
    path('intermediates/', view=views.intermediates)
    # path('doctors/', view=views.get_doctors_by_speciality),
    # path('verify-otp/', view=views.verify_OTP),
]


