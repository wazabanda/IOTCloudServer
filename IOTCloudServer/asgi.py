"""
ASGI config for IOTCloudServer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import core.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IOTCloudServer.settings")
# websocket_urlpatterns = [
#     re_path(r'ws/some_path/$', MyConsumer.as_asgi()),
# ]
application = get_asgi_application()
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             core.routing.websocket_urlpatterns
#             # your websocket routing goes here
#         )
#     ),
# })