from django.urls import path, include
from . import views
from chatApp.routing import websocket_urlpatterns

urlpatterns = [
    path('', views.index),
    path('<str:room_name>/', view=views.lobby)
]


