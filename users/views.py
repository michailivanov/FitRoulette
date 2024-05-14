from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import LoginUserForm, RegisterUserForm
from django.views.generic import CreateView

# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Вход в качестве хоста игры'}

    def get_success_url(self):
        return reverse_lazy('main_page')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')