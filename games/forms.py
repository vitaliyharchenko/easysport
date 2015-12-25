# coding=utf-8
from django import forms
from django.forms import inlineformset_factory
from .models import Game, UserGameAction


class UserGameActionForm(forms.ModelForm):
    class Meta:
        model = UserGameAction
        fields = ('user', 'game',)

    VISITED = 5
    NOTVISITED = 6
    NOTPAY = 7
    ACTIONS = (
        (VISITED, 'Посетил и заплатил'),
        (NOTVISITED, 'Не пришел'),
        (NOTPAY, 'Посетил, но не заплатил')
    )

    action = forms.ChoiceField(choices=ACTIONS)


GameFormSet = inlineformset_factory(Game, UserGameAction, form=UserGameActionForm, can_delete=False, extra=0)