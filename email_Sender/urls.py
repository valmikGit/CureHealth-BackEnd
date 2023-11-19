from django.urls import path
from email_Sender import views

urlpatterns = [
    path('', view=views.get_Routes),
    path('send-email/', view=views.send_Email)
]
