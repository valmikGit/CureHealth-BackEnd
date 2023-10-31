from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/socket-server/', ChatConsumer.as_asgi())
]

# websocket_urlpatterns = [
#     re_path(r'ws/socket-server/', ChatConsumer.as_asgi())
# ]
<<<<<<< HEAD

websocket_urlpatterns = [
    path('ws/socket-server/', consumers.ChatConsumer.as_asgi())
]
=======
>>>>>>> 4887b4cb9420e27a7f11bf66c6eddb00cab5ebb4
