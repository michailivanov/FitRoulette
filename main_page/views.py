from random import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import CardSet, Exercise, GameSession


def title(request):
    return render(request, 'title.html')


def settings(request):
    return render(request, 'settings.html')


def card_sets(request):
    if request.method == 'POST':
        card_set_id = request.POST.get('set_id')
        card_set = CardSet.objects.get(id=card_set_id)
        game_session = GameSession.objects.create(card_set=card_set)
        return HttpResponseRedirect(reverse('game_session', args=[str(game_session.session_id)]))

    sets = CardSet.objects.all()
    return render(request, 'card_sets.html', {'sets': sets})


def game_session(request, session_id):
    game = GameSession.objects.get(session_id=session_id)
    return render(request, 'game_session.html', {'game': game})


def start_game(request, session_id):
    game = GameSession.objects.get(session_id=session_id)
    if request.method == 'POST':
        # Spin the fitness roulette wheel
        exercises = list(game.card_set.exercises.all())
        game.current_exercise = random.choice(exercises)
        game.save()
        # Update current player
        current_player_index = list(game.players.all()).index(game.current_player)
        next_player_index = (current_player_index + 1) % len(game.players.all())
        game.current_player = list(game.players.all())[next_player_index]
        game.save()
        # Send real-time update
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'game_{}'.format(game.id),
            {
                'type': 'update_exercise',
                'exercise': game.current_exercise.to_json(),
            }
        )
    return render(request, 'play_game.html', {'game': game})


