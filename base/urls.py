from django.contrib import admin
from django.urls import path, include
from base import views

urlpatterns = [
    path('', view=views.lobby),
    path('room/', view=views.room),
    path('get_token/', views.getToken),
    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
    path('register/', include('healthcare.urls')),
    path('healthcare_api/', include('healthcare.healthcare_api.urls'))
]