from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/socket-server/', ChatConsumer.as_asgi())
]

# websocket_urlpatterns = [
#     re_path(r'ws/socket-server/', ChatConsumer.as_asgi())
# ]
