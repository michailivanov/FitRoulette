from django.urls import path
from . import views

urlpatterns = [
    path('', views.title, name='main_page'),
    path('settings', views.settings, name='settings'),
    path('card_sets', views.card_sets, name='card_sets'),
    path('game_session/<uuid:session_id>/', views.game_session, name='game_session'),
    path('start_game/<uuid:session_id>/', views.start_game, name='start_game'),
    path('add_exercise', views.add_exercise, name='add_exercise'),
    path('add_cardset', views.add_cardset, name='add_cardset'),
    #path('card_sets_json', views.card_sets_json, name='card_sets_json')
    path('card_sets_json', views.CardsAndImagesView, name='card_sets_json'),
    path('second_endpoint_json', views.SecondEndpoint) # Я не знаю как назвать, так как будут отправлены два объекта
]
