from django.shortcuts import render
from .models import CardSet, Exercise


def title(request):
    return render(request, 'main_page/title.html')


def settings(request):
    return render(request, 'main_page/settings.html')


def card_sets(request):
    sets = CardSet.objects.all()
    return render(request, 'main_page/card_sets.html', {'sets': sets})

