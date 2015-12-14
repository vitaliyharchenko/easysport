# coding=utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.utils import timezone
from .forms import UserLoginForm, UserRegistrationForm
from .models import User, UserActivation
from utils import mailing
import hashlib
import random


def login_view(request):
    if request.user.is_authenticated():
        return redirect('index_view')
    if request.method == "POST":
        form = UserLoginForm(request.POST or None)
        if form.is_valid:
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=email, password=password)
            # TODO: добавить условия, при которых юзер не может залогиниться
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('index_view')
                else:
                    messages.warning(request, "Ваш профиль деактивирован!")
            else:
                    messages.warning(request, "Введенные данные неверны!")
    else:
        form = UserLoginForm(request)

    return render(request, 'login.html', {"form": form})


def logout_view(request):
    return_path = request.META.get('HTTP_REFERER', '/')
    auth.logout(request)
    return redirect(return_path)


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if request.user.is_authenticated():
        return redirect('login_view')
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()
            user = User.objects.get(email=email)
            UserActivation.objects.filter(user=user).delete()

            new_activation = UserActivation(user=user, activation_key=activation_key,
                                            request_time=timezone.now())
            new_activation.save()
            mailing.confirm_email(email, activation_key)

            user = auth.authenticate(username=email, password=password)
            auth.login(request, user)

            return redirect('index_view')
        else:
            messages.warning(request, "Form is not valid!")
            return render(request, 'reg.html', {'form': form})
    return render(request, 'reg.html', {'form': form})


def register_confirm(request, activation_key):
    # TODO: страница ошибки активации
    user_profile = UserActivation.objects.get(activation_key=activation_key)

    if user_profile.count() == 0:
         # TODO: страница ошибки активации
        raise Exception("Неверный код")
    else:
        user = user_profile.user
        user.is_active = True
        user.save()
        if not request.user.is_authenticated():
            user = auth.authenticate(username=user.email, password=user.password)
            auth.login(request, user)

        # TODO: send thanks-message on email
        return redirect('index_view')