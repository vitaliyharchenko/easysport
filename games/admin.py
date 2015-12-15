# coding=utf-8
from django.contrib import admin
from .models import Game, UserGameAction


# Register your models here.
class UserGameActionInline(admin.TabularInline):
    model = UserGameAction
    extra = 0


# TODO: delete created_by field
# TODO: add datetime picker widget
class GameAdmin(admin.ModelAdmin):
    model = Game
    inlines = [UserGameActionInline]

    def save_model(self, request, obj, form, change):
        user = request.user
        obj.created_by = user
        obj.save()


admin.site.register(Game, GameAdmin)