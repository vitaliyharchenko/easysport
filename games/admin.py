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
    list_display = ('id', 'datetime', 'gametype', 'court', 'capacity', 'responsible_user', 'is_reported')

    def has_add_permission(self, request):
        if request.user.is_admin or request.user.is_organizer:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin or request.user.is_organizer:
            return True
        else:
            return False

    def has_module_permission(self, request):
        if request.user.is_admin or request.user.is_organizer:
            return True
        else:
            return False

    def save_model(self, request, obj, form, change):
        user = request.user
        sporttype = GameType.objects.get(pk=obj.gametype.id).sporttype
        obj.sporttype = sporttype
        obj.created_by = user
        obj.save()


admin.site.register(Game, GameAdmin)