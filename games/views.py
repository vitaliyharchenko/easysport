# coding=utf-8
import json
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import datetime
from .models import Game, UserGameAction
from users.models import User
from sports.models import SportType
from .forms import GameFormSet, ActionFormSet, GameEditForm, GameCreationForm
from utils import mailing

from django.core import serializers


# Create your views here.
def games_view(request):
    context = dict()
    sport_types = SportType.objects.all()
    context['sport_types'] = sport_types

    try:
        query = int(request.GET.__getitem__('q'))
        # my games
        if query == -3:
            user = User.objects.get(email=request.user.email)
            games_ids = UserGameAction.objects.filter(user=user, game__datetime__gt=timezone.now()).values_list('game', flat=True)
            context['games'] = Game.objects.filter(pk__in=games_ids).order_by('datetime')
        # needs report
        elif query == -2:
            user = User.objects.get(email=request.user.email)
            context['games'] = Game.objects.filter(is_reported=False, responsible_user=user,
                                                   datetime__lt=timezone.now(), deleted=False).order_by('-datetime')
        # old games
        elif query == -1:
            context['games'] = Game.objects.filter(is_reported=True, datetime__lt=timezone.now(), deleted=False).order_by('-datetime')
        # all feature games
        else:
            time_mark = timezone.now() - datetime.timedelta(hours=2)
            context['games'] = Game.objects.filter(is_public=True, sporttype=query, datetime__gt=time_mark,
                                                   deleted=False).order_by('datetime')
        context['query'] = query
        return render(request, 'games.html', context)
    except KeyError:
        time_mark = timezone.now() - datetime.timedelta(hours=2)
        context['games'] = Game.objects.filter(is_public=True, is_reported=False, datetime__gt=time_mark,
                                               deleted=False).order_by('datetime')
        return render(request, 'games.html', context)


def game_view(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'game.html', {'game': game, 'standalone': True})


def game_create_view(request):
    if request.user.is_organizer:
        now = timezone.localtime(timezone.now() + timezone.timedelta(days=2))
        form = GameCreationForm(initial={'datetime': now, 'datetime_to': now, 'created_by': request.user})

        if request.method == "POST":
            form = GameCreationForm(request.POST)
            if form.is_valid():
                form.save()
                game = Game.objects.filter(created_by=request.user).order_by('-id')[0]
                return redirect('game_view', game.pk)
            else:
                print(form.errors)
        return render(request, 'game_create.html', {'form': form})
    else:
        return redirect('index_view')


def game_edit_view(request, game_id):
    UserGameActionInlineFormset = inlineformset_factory(Game, UserGameAction, fields=('user', 'action', 'game'),
                                                        extra=1, can_delete=True)

    if request.method == "POST":
        game = Game.objects.get(id=game_id)
        form = GameEditForm(request.POST, instance=game)
        formset = UserGameActionInlineFormset(request.POST, instance=game)
        print(form)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('game_view', game_id)
        else:
            notification = Notification(user=request.user,
                                        text='Ошибка при редактировании игры')
            notification.save()
            return redirect('game_view', game_id)
    else:
        game = Game.objects.get(id=game_id)
        form = GameEditForm(instance=game)
        formset = UserGameActionInlineFormset(instance=game)
        return render(request, 'game_edit.html', {'game': game, 'form': form, 'formset': formset})


def game_next_add(request, game_id):
    game = Game.objects.get(id=game_id)
    game.datetime = game.datetime + datetime.timedelta(days=7)
    game.datetime_to = game.datetime_to + datetime.timedelta(days=7)
    game.pk = None
    game.is_reported = False
    game.save()
    # TODO: already exist check
    return redirect('games_view')


# TODO: privacy add
def game_roster_view(request, game_id):
    context = {'game': Game.objects.get(id=game_id)}
    return render(request, 'roster.html', context)


# TODO: privacy add
def game_invite_view(request, game_id):
    game = Game.objects.get(id=game_id)
    context = {'game': game, 'old_users': game.old_users}
    return render(request, 'invite.html', context)


def game_email_invite(request, game_id):
    game = Game.objects.get(id=game_id)
    for user in game.old_users():
        pass
        mailing.invite_email(user, game)
    return redirect('game_invite_view', game_id)


# TODO: privacy add
def game_report_view(request, game_id):
    game = Game.objects.get(id=game_id)

    if request.method == "POST":
        formset = ActionFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            game.is_reported = True
            game.save()
            return redirect('game_view', game_id)
    else:
        formset = ActionFormSet(queryset=UserGameAction.objects.filter(game=game).filter(action=UserGameAction.SUBSCRIBED))

    context = {'game': game, 'formset': formset}
    return render(request, 'report.html', context)


# Return error for ajax
def error_response(description):
    error = {'error_description': description}
    return HttpResponse(json.dumps({'error': error}), content_type="application/json")


# TODO: error alert
@require_POST
def gameaction(request):
    if request.is_ajax():
        action = request.POST["action"]
        game_id = request.POST["game_id"]
        if request.user.is_authenticated():
            user = User.objects.get(email=request.user.email)
            game = Game.objects.get(id=game_id)

            if action == 'subscribe':
                set_action = UserGameAction.SUBSCRIBED
            elif action == 'unsubscribe':
                set_action = UserGameAction.UNSUBSCRIBED
            elif action == 'reserve':
                set_action = UserGameAction.RESERVED
            elif action == 'unreserve':
                set_action = UserGameAction.UNRESERVED
            try:
                usergameaction = UserGameAction.objects.get(game=game, user=user)
                current_action = usergameaction.action
                if current_action == set_action:
                    return error_response('Action already save')
                else:
                    # TODO: add check of game in similar time
                    if set_action == UserGameAction.SUBSCRIBED and not game.has_place:
                        return error_response('There is no place now')
                    elif set_action == UserGameAction.RESERVED and not game.has_reserved_place:
                        return error_response('There is no place now')
                    usergameaction.action = set_action
                    usergameaction.save()

                    return render(request, 'tagtemplates/game_tpl.html', {'game': game, 'current_user': user})
            except UserGameAction.DoesNotExist:
                UserGameAction.objects.create(game=game, user=user, action=set_action)
                # TODO: email user
                return render(request, 'tagtemplates/game_tpl.html', {'game': game, 'current_user': user})
        else:
            return error_response('Not auth')
    else:
        return error_response('Not AJAX')
