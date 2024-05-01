from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_game_session, name='create_game_session'),
    path('<int:pk>', views.GameSessionView.as_view(), name='game-session')
]