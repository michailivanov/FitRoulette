from django.shortcuts import render
from .models import CardSet, Exercise, GameSession


def title(request):
    return render(request, 'title.html')


def settings(request):
    return render(request, 'settings.html')


def card_sets(request):
    sets = CardSet.objects.all()
    return render(request, 'card_sets.html', {'sets': sets})


def create_game_session(request):
    session = GameSession()
    return render(request, 'create_game_session.html', {'session': session})



