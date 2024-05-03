from django.urls import path
from . import views

urlpatterns = [
    path('', views.title, name='main_page'),
    path('settings', views.settings, name='settings'),
    path('card_sets', views.card_sets, name='card_sets'),
    path('game_session/<uuid:session_id>/', views.game_session, name='game_session'),
]