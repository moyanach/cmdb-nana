from django.urls import path
from webshell.views import SSHConsumer

webshell_urlpatterns = [
    path(r'ws/shell/', SSHConsumer.as_asgi()),
]
