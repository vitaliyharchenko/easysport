# coding=utf-8
from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import Game, UserGameAction, GameType


class UserGameActionForm(forms.ModelForm):
    class Meta:
        model = UserGameAction
        fields = ('user', 'action',)
        exclude = ('id',)
        readonly_fields = ('user', )

    VISITED = 5
    NOTVISITED = 6
    NOTPAY = 7
    ACTIONS = (
        (VISITED, 'Посетил и заплатил'),
        (NOTVISITED, 'Не пришел'),
        (NOTPAY, 'Посетил, но не заплатил')
    )

    action = forms.ChoiceField(choices=ACTIONS)


ActionFormSet = modelformset_factory(UserGameAction, fields=('user', 'action',), exclude=('id',), extra=0,
                                     form=UserGameActionForm)


GameFormSet = inlineformset_factory(Game, UserGameAction, form=UserGameActionForm, can_delete=False,
                                    fields=('user', 'action',), extra=0)


class GameEditForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'responsible_user', 'coach', 'court', 'gametype',
                  'capacity', 'cost', 'datetime', 'datetime_to', 'reserved_count', 'deleted', 'is_public']


class GameCreationForm(forms.ModelForm):

    class Meta:
        model = Game
        exclude = ('sporttype', 'is_reported', 'deleted',)
        widgets = {'created_by': forms.HiddenInput()}

    def save(self, commit=True):
        obj = super(GameCreationForm, self).save(commit=False)
        sporttype = GameType.objects.get(pk=obj.gametype.id).sporttype
        obj.sporttype = sporttype
        obj.save()
