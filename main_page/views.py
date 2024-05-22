from random import shuffle, choice

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import CardSet, Exercise, GameSession
from .forms import AddExerciseForm, AddCardSetForm
from .serializers import CardSetSerializer, ExerciseSerializer, GameSessionSerializer


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


def card_sets_json(request):
    card_sets = CardSet.objects.all().values('id', 'name')
    data = list(card_sets)
    return JsonResponse(data, safe=False)


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

@api_view(['GET','POST'])
def CardsAndImagesView(request):
    cards = CardSet.objects.all()
    images = Exercise.objects.all()

    pks = GameSession.objects.values_list('pk', flat=True)
    random_pk = choice(pks)
    game = GameSession.objects.get(pk=random_pk)

    cards_serializer = CardSetSerializer(cards, many=True)
    images_serializer = ExerciseSerializer(images, many=True, context={"request": request})
    game_serializer = GameSessionSerializer(game, context={"request": request})

    return Response({
        "cards": cards_serializer.data,
        "images": images_serializer.data,
        "game": game_serializer.data,
    })


#Я не знаю как назвать второй эндпоинт, поэтому назову так
@api_view(['GET'])
def SecondEndpoint(request):

    # Получаем FormData
    name = request.data.getlist('FormData[0]')
    name_serializer = ExerciseSerializer.get_names(name, many=True)

    image = request.data.getlist('FormData[1]')
    images_serializer = ExerciseSerializer.get_images(image, many=True)

    # Для получения наборов
    cards = request.data.get('card_sets')
    cards_serializer = CardSetSerializer(cards, many=True)

    return Response(
                    {"name": name_serializer.data, "image": images_serializer.data},
                    {"cards": cards_serializer.data},
    )