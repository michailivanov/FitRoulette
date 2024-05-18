from random import shuffle

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import CardSet, Exercise, GameSession
from .forms import AddExerciseForm, AddCardSetForm


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


@login_required
def add_exercise(request):
    if request.method == 'POST':
        form = AddExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            image = form.cleaned_data.get('image')
            form.save()
            messages.success(request, 'Упражнение добавлено!')
            return redirect('card_sets')
        else:
            form = AddExerciseForm(request.POST)
            messages.success(request, 'Ошибка в добавлении упражнения')
            return render(request, 'add_exercise.html', {'form': form})
    else:
        form = AddExerciseForm()
        return render(request, 'add_exercise.html', {'form': form})


@login_required
def add_cardset(request):
    if request.method == 'POST':
        form = AddCardSetForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            exercises = form.cleaned_data.get('exercises')
            form.save()
            messages.success(request, 'Набор добавлен!')
            return redirect('card_sets')
        else:
            form = AddCardSetForm(request.POST)
            messages.success(request, 'Ошибка в добавлении набора')
            return render(request, 'add_cardset.html', {'form': form})
    else:
        form = AddCardSetForm()
        return render(request, 'add_cardset.html', {'form': form})
