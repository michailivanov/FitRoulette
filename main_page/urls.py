from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = ([
    path('', views.title, name='main_page'),
    path('settings', views.settings, name='settings'),
    path('card_sets', views.card_sets, name='card_sets'),
    path('game_session/<uuid:session_id>/', views.game_session, name='game_session'),
    path('start_game/<uuid:session_id>/', views.start_game, name='start_game'),
    path('add_exercise', views.add_exercise, name='add_exercise'),
    path('add_cardset', views.add_cardset, name='add_cardset'),
    path('delete_cardset', views.delete_cardset, name='delete_cardset'),
    path('edit_cardset', views.edit_cardset, name='edit_cardset'),
    path('delete_exercise', views.delete_exercise, name='delete_exercise'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
               static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
