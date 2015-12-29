# coding=utf-8
from django.shortcuts import render, redirect
from django.core import signing
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.http import Http404
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ChangePasswordForm
from .models import User, UserActivation
from utils import mailing, vkontakte
from urllib.request import urlopen
from io import BytesIO
from django.core.files import File


@csrf_protect
def login_view(request):
    if request.user.is_authenticated():
        return redirect('index_view')

    shortcut = lambda: render(request, 'login.html', {"form": form})
    return_path = request.META.get('HTTP_REFERER', '/')

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
                    return redirect(return_path)
                else:
                    messages.warning(request, "Ваш профиль деактивирован!")
                    return shortcut()
            else:
                messages.warning(request, "Введенные данные неверны!")
                return shortcut()
        else:
            messages.warning(request, "Введенные данные некорректны!")
            return shortcut()

    elif 'code' in request.GET:
        code = request.GET['code']
        form = UserLoginForm(request.POST or None)
        try:
            access_token, user_id = vkontakte.auth_code(code, reverse('login_view'))
        except vkontakte.AuthError as e:
            messages.warning(request, u'Ошибка OAUTH авторизации {}'.format(e))
            return shortcut()
        try:
            user = User.objects.get(vkuserid=user_id)

            # Bug fix
            user.last_login = timezone.now()
            user.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return redirect(return_path)
        except User.DoesNotExist:
            messages.warning(request, 'Такой пользователь не найден')
            return shortcut()

    else:
        form = UserLoginForm(request)
        return shortcut()


def logout_view(request):
    auth.logout(request)
    return redirect('index_view')


def register_view(request):
    form = UserRegistrationForm(request.POST or None, request.FILES or None)
    if request.user.is_authenticated():
        return redirect('login_view')
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            activation_key = signing.dumps({'email': email})
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
            messages.warning(request, "Здесь есть неверно заполненные поля!")
            return render(request, 'reg.html', {'form': form})
    return render(request, 'reg.html', {'form': form})


def vk_reg(request):
    if 'code' in request.GET:
        code = request.GET['code']
        try:
            access_token, user_id = vkontakte.auth_code(code, reverse('vk_reg'))
        except vkontakte.AuthError as e:
            messages.warning(request, u'Ошибка OAUTH авторизации {}'.format(e), extra_tags='integration')
            return redirect('reg_view')
        try:
            user = User.objects.get(vkuserid=user_id)
            user.last_login = timezone.now()
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return redirect('user_update_view')
        except User.DoesNotExist:
            vkuser = vkontakte.api(access_token, 'users.get', fields=['sex', 'bdate', 'city',
                                                                      'photo_max', 'contacts'])[0]
            vkdata = dict()
            vkdata['vkuserid'] = user_id
            vkdata['first_name'] = vkuser['first_name']
            vkdata['last_name'] = vkuser['last_name']

            if 'mobile_phone' in vkuser:
                vkdata['phone'] = vkuser['mobile_phone']
            elif 'home_phone' in vkuser:
                vkdata['phone'] = vkuser['home_phone']
            else:
                vkdata['phone'] = None

            if vkuser['sex']:
                if vkuser['sex'] == 2:
                    vkdata['sex'] = 'm'
                elif vkuser['sex'] == 1:
                    vkdata['sex'] = 'f'
            else:
                vkdata['sex'] = None

            if 'bdate' in vkuser:
                if len(vkuser['bdate']) >= 8:
                    vkdata['bdate'] = vkuser['bdate']
                elif vkuser['bdate'] != '':
                    messages.warning(request, 'Неполная дата')
                    vkdata['bdate'] = vkuser['bdate']
            else:
                vkdata['bdate'] = ''

            # TODO: set vkontakteavatar
            if 'photo_max' in vkuser:
                url = vkuser['photo_max']
                response = urlopen(url)
                io = BytesIO(response.read())
                file = File(io)
                vkdata['avatar'] = file

            initial = {'sex': vkdata['sex'],
                       'first_name': vkdata['first_name'],
                       'last_name': vkdata['last_name'],
                       'phone': vkdata['phone'],
                       'bdate': vkdata['bdate'],
                       'vkuserid': user_id,
                       'avatar': vkdata['avatar']
                       }

            form = UserRegistrationForm(initial=initial)
            return render(request, 'reg.html', {'form': form})


def register_confirm(request, activation_key):
    user_profile = UserActivation.objects.get(activation_key=activation_key)

    if not user_profile:
        # TODO: страница ошибки активации
        raise Exception("Неверный код")
    else:
        user = user_profile.user
        user.is_active = True
        user.save()
        if not request.user.is_authenticated():
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            # TODO: page of success activation
        # TODO: send thanks-message on email
        return redirect('index_view')


def user_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise Http404("Такого пользователя не существует")
    context = {'user': user}

    if request.user.pk == user.pk:
        context['current'] = True
    return render(request, 'user.html', context)


def users_view(request):
    try:
        query = request.GET.__getitem__('q')
        users = User.objects.filter(first_name__icontains=query) | User.objects.filter(last_name__icontains=query)
        context = {'users': users, 'query': query}
    except KeyError:
        context = {'users': User.objects.all().order_by('-last_login')}
    return render(request, 'users.html', context)


@login_required
def user_update_view(request):
    user = User.objects.get(email=request.user.email)
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user)

    if 'code' in request.GET:
        code = request.GET['code']
        try:
            access_token, user_id = vkontakte.auth_code(code, reverse('user_update_view'))
        except vkontakte.AuthError as e:
            messages.warning(request, u'Ошибка OAUTH авторизации {}'.format(e), extra_tags='integration')
            return redirect('user_update_view')
        try:
            user = User.objects.get(vkuserid=user_id)
            messages.warning(request, 'Этот аккаунт ВКонтакте уже связан с профилем', extra_tags='integration')
            return redirect('user_update_view')
        except User.DoesNotExist:
            user = User.objects.get(email=request.user.email)
            user.vkuserid = user_id
            user.save()
            messages.success(request, "Профиль ВКонтакте прикреплен", extra_tags='integration')
            return redirect('user_update_view')

    elif request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, "Успешно сохранено!", extra_tags='info')
            return redirect('user_update_view')
        else:
            messages.warning(request, "Некорректные данные", extra_tags='info')
    return render(request, 'user_update.html', {'form': form, 'pass_form': ChangePasswordForm})


@login_required
def changepass(request):
    user = User.objects.get(email=request.user.email)
    pass_form = ChangePasswordForm(request.POST or None)
    if request.method == 'POST':
        if pass_form.is_valid():
            password = pass_form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            validation = auth.authenticate(username=user.email, password=password)
            auth.login(request, validation)
            messages.success(request, "Пароль изменен", extra_tags='changepass')
        else:
            messages.warning(request, "Введенные пароли некорректны!", extra_tags='changepass')
    return redirect('user_update_view')


@login_required
def unsetvkid(request):
    user = User.objects.get(email=request.user.email)
    user.vkuserid = None
    user.save()
    messages.success(request, "Профиль ВКонтакте откреплен", extra_tags='integration')
    return redirect('user_update_view')