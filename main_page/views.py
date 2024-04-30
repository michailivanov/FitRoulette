from django.shortcuts import render
from django.http import HttpResponse


def title(request):
    return render(request, 'main_page/title.html')


def settings(request):
    return render(request, 'main_page/settings.html')


def card_sets(request):
    return render(request, 'main_page/card_sets.html')