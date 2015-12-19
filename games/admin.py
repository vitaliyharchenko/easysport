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
    exclude = ('sporttype',)
    readonly_fields = ('created_by',)
    list_display = ('id', 'datetime', 'gametype', 'court', 'capacity', 'responsible_user', 'created_by', 'is_reported')

    def has_add_permission(self, request):
        return permissions.admin_organizer_permissions(request)

    def has_change_permission(self, request, obj=None):
        if request.user:
            if request.user.is_admin or request.user.is_organizer or request.user.is_responsible:
                if obj is None:
                    return True
                else:
                    if obj.responsible_user == request.user or obj.created_by == request.user or request.user.is_admin or request.user.is_superuser:
                        return True
                    else:
                        return False
            else:
                return False
        else:
            return False
        # return permissions.admin_organizer_permissions(request)

    def has_module_permission(self, request):
        return permissions.admin_organizer_permissions(request)

    def save_model(self, request, obj, form, change):
        user = request.user
        sporttype = GameType.objects.get(pk=obj.gametype.id).sporttype
        obj.sporttype = sporttype
        obj.created_by = user
        obj.save()


admin.site.register(Game, GameAdmin)