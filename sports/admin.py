from django.contrib import admin
from .models import SportType, GameType, Amplua


class GameTypeInline(admin.TabularInline):
    model = GameType
    extra = 0


class AmpluaInline(admin.TabularInline):
    model = Amplua
    extra = 0


class SportTypeAdmin(admin.ModelAdmin):
    model = SportType
    inlines = [GameTypeInline, AmpluaInline]


# Register your models here.
admin.site.register(SportType, SportTypeAdmin)