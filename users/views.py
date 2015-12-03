# coding=utf-8
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .forms import UserLoginForm


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        # TODO: global name for index url
        return redirect('/')
    if request.method == "POST":
        form = UserLoginForm(request.POST or None)
        if form.is_valid:
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=email, password=password)
            # TODO: добавить условия, при которых юзер не может залогиниться  and user.is_active
            if user:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.warning(request, "Упс! Введенные данные неверны!")
    else:
        form = UserLoginForm(request)

    template = "login.html"
    context = {"form": form}
    return render(request, template, context)


def logout_view(request):
    auth.logout(request)
    # TODO: global name for login url
    return redirect("/login/")