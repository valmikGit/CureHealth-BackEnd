from django.urls import re_path, path
from chatApp.consumers import ChatConsumer

# websocket_urlpatterns = [
#     re_path(r'ws/socket-server/', ChatConsumer.as_asgi())
# ]

websocket_urlpatterns = [
    path('ws/socket-server/', ChatConsumer.as_asgi())
]