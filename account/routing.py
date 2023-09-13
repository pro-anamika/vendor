
from django.urls import re_path
from account import consumers

websocket_urlpatterns = [
    # re_path(r'ws/admin-notifications/$', consumers.AdminNotificationConsumer.as_asgi()),
    re_path('ws/chat/kl/',consumers.ChatConsumer.as_asgi()),
]
