from django.urls import path
from . import consumers

ws_urlpatterns = [
    path("ws/game_session/<uuid:session_id>/", consumers.GameSessionConsumer.as_asgi()),
]
