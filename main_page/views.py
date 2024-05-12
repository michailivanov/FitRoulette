from random import shuffle

from django.shortcuts import render, redirect

from .models import CardSet, Exercise, GameSession


def title(request):
    return render(request, 'title.html')


def settings(request):
    return render(request, 'settings.html')


def card_sets(request):
    if request.method == 'POST':
        card_set_id = request.POST.get('set_id')
        card_set = CardSet.objects.get(id=card_set_id)
        exercises = list(card_set.exercises.all())
        shuffle(exercises)
        # Создаем список словарей для JSONField
        shuffled_exercises = [{'id': ex.id, 'name': ex.name} for ex in exercises]
        game_session = GameSession.objects.create(card_set=card_set, shuffled_exercises=shuffled_exercises)
        return redirect('game_session', session_id=str(game_session.session_id))

    sets = CardSet.objects.all()
    return render(request, 'card_sets.html', {'sets': sets})


def game_session(request, session_id):
    game = GameSession.objects.get(session_id=session_id)
    return render(request, 'game_session.html', {'game': game})


def shuffle_cards(exercises):
    exercises_list = list(exercises)
    shuffle(exercises_list)
    return exercises_list


def start_game(request, session_id):
    game = GameSession.objects.get(session_id=session_id)
    return render(request, 'start_game.html', {
        'game': game,
    })


