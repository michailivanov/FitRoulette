import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from main_page.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FitRoulette.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(ws_urlpatterns)
    )
})
