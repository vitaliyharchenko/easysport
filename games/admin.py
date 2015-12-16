# coding=utf-8
from django.contrib import admin
from .models import Game, UserGameAction
from sports.models import GameType


# Register your models here.
class UserGameActionInline(admin.TabularInline):
    model = UserGameAction
    extra = 0


# TODO: add datetime picker widget
class GameAdmin(admin.ModelAdmin):
    model = Game
    inlines = [UserGameActionInline]
    exclude = ('created_by', 'sporttype',)

    def save_model(self, request, obj, form, change):
        user = request.user
        sporttype = GameType.objects.get(pk=obj.gametype.id).sporttype
        obj.sporttype = sporttype
        obj.created_by = user
        obj.save()


admin.site.register(Game, GameAdmin)