# coding=utf-8
import json
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Game, UserGameAction
from users.models import User
from sports.models import SportType


# Create your views here.
def games_view(request):
    context = dict()
    sport_types = SportType.objects.all()
    context['sport_types'] = sport_types
    if not request.user.is_authenticated():
        return redirect('login_view')
    else:
        try:
            query = int(request.GET.__getitem__('q'))
            if query == -2:
                user = User.objects.get(email=request.user.email)
                context['games'] = Game.objects.filter(is_reported=False, responsible_user=user, datetime__lt=timezone.now(), deleted=False)
            elif query == -1:
                context['games'] = Game.objects.filter(is_reported=True, deleted=False)
            else:
                context['games'] = Game.objects.filter(sporttype=query, datetime__gt=timezone.now(), deleted=False)
            context['query'] = query
            return render(request, 'games.html', context)
        except KeyError:
            context['games'] = Game.objects.filter(is_reported=False, datetime__gt=timezone.now(), deleted=False)
            return render(request, 'games.html', context)


def game_view(request, game_id):
    context = {}
    game = Game.objects.get(id=game_id)
    user = User.objects.get(email=request.user.email)
    if game.responsible_user == user:
        context['need_report'] = True
    context['game'] = game
    context['standalone'] = True
    return render(request, 'game.html', context)


# TODO: privacy add
def game_roster_view(request, game_id):
    context = {'game': Game.objects.get(id=game_id)}
    return render(request, 'roster.html', context)


# TODO: privacy add
def game_invite_view(request, game_id):
    game = Game.objects.get(id=game_id)
    court = game.court
    sporttype = game.sport_type

    games = Game.objects.filter(court=court, sporttype_id=sporttype, is_reported=True)
    old_users = list()
    for game in games:
        old_users += game.visited

    old_users = list(set(old_users))

    context = {'game': Game.objects.get(id=game_id), 'old_users': old_users}
    return render(request, 'invite.html', context)


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
                    # TODO: email user
                    return render(request, 'tagtemplates/game_tpl.html', {'game': game, 'current_user': user})
            except UserGameAction.DoesNotExist:
                UserGameAction.objects.create(game=game, user=user, action=set_action)
                # TODO: email user
                return render(request, 'tagtemplates/game_tpl.html', {'game': game, 'current_user': user})
        else:
            return error_response('Not auth')
    else:
        return error_response('Not AJAX')