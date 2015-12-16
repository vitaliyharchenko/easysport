# coding=utf-8

from django import template
from games.models import UserGameAction

register = template.Library()


@register.inclusion_tag('tagtemplates/game_tpl.html', takes_context=True)
def game_tpl(context, game):
    newcontext = {'game': game,
                  'current_user': context['current_user']}
    try:
        newcontext['standalone'] = context['standalone']
    except KeyError:
        pass
    return newcontext


# находит объект подписи на игру для заданной игры и пользователя
@register.assignment_tag
def usergameaction(user, game):
    try:
        action = UserGameAction.objects.get(game=game, user=user)
    except UserGameAction.DoesNotExist:
        return None
    return action.action