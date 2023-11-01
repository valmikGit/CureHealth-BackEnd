from django.urls import path
from agora import views
urlpatterns = [
    path('', view=views.get_Agora_Routes),
    path('index/', views.index, name='agora-index'),
    path('pusher/auth/', views.pusher_auth, name='agora-pusher-auth'),
    path('token/', views.generate_agora_token, name='agora-token'),
    path('call-user/', views.call_user, name='agora-call-user'),
]