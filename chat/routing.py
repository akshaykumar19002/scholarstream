from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.auth import AuthMiddlewareStack
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', consumers.ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)),
})
