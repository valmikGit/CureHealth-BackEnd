"""
ASGI config for Synergy_Backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Synergy_Backend.settings')

# application = get_asgi_application()

# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path
# from chatApp.consumers import ChatConsumer
# from channels.auth import AuthMiddlewareStack
# from chatApp.routing import websocket_urlpatterns


# ws_pattern = [
#     path('chat/<room_code>', ChatConsumer.as_asgi())
# ]

# # application = ProtocolTypeRouter(
# #     {
# #         'websocket' : (URLRouter(ws_pattern))
# #     }
# # )

# application = ProtocolTypeRouter(
#     {
#         'websocket' : AuthMiddlewareStack(
#             URLRouter(websocket_urlpatterns)
#         )
#     }
# )


import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chatApp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')

# application = ProtocolTypeRouter({
#     'http':get_asgi_application(),
#     'websocket':AuthMiddlewareStack(
#         URLRouter(
#             chatApp.routing.websocket_urlpatterns
#         )
#     )
# })

application = ProtocolTypeRouter({
    'ws':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            chatApp.routing.websocket_urlpatterns
        )
    )
})