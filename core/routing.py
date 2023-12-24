from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
    # path('ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi())
    path('ws/devices/<uuid:uuid>', consumers.DeviceConsumer.as_asgi())
]
