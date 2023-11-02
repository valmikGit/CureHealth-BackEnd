from django.urls import path
from verifyAuth import views

urlpatterns = [
    path('', view=views.get_Routes),
    path('verify-otp/', view=views.verify_otp),
    path('send-otp/', view=views.send_otp)
]
