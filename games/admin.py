# coding=utf-8
from django.contrib import admin
from .models import Game, UserGameAction
from sports.models import GameType
from utils import permissions


# Register your models here.
class UserGameActionInline(admin.TabularInline):
    model = UserGameAction
    extra = 0


class GameAdmin(admin.ModelAdmin):
    model = Game
    inlines = [UserGameActionInline]
    exclude = ('created_by', 'sporttype',)
    list_display = ('id', 'datetime', 'gametype', 'court', 'capacity', 'responsible_user', 'created_by', 'is_reported')

    def has_add_permission(self, request):
        return permissions.admin_organizer_permissions(request)

    def has_change_permission(self, request, obj=None):
        return permissions.admin_organizer_responsible_permissions(request)

    def has_module_permission(self, request):
        return permissions.admin_organizer_permissions(request)

    def save_model(self, request, obj, form, change):
        user = request.user
        sporttype = GameType.objects.get(pk=obj.gametype.id).sporttype
        obj.sporttype = sporttype
        obj.created_by = user
        obj.save()


admin.site.register(Game, GameAdmin)