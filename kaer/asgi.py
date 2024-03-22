"""
ASGI config for kaer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

# from channels.http import AsgiHandler
# from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application


from webshell.routing import webshell_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj32_example.settings')

# application = get_asgi_application()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        webshell_urlpatterns
    )
})
