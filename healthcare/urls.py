from django.contrib import admin
from django.urls import path
from healthcare import views

urlpatterns = [
    path('', view=views.home),
    path('doctors/', view=views.doctors),
    path('patients/', view=views.patients),
    path('allusers/', view=views.new_Users)
]