from django.contrib import admin
from .models import SportType, GameType, Amplua


class GameTypeInline(admin.TabularInline):
    model = GameType
    extra = 0

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        else:
            return False

    def has_module_permission(self, request):
        if request.user.is_admin:
            return True
        else:
            return False


class AmpluaInline(admin.TabularInline):
    model = Amplua
    extra = 0

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        else:
            return False

    def has_module_permission(self, request):
        if request.user.is_admin:
            return True
        else:
            return False


class SportTypeAdmin(admin.ModelAdmin):
    model = SportType
    inlines = [GameTypeInline, AmpluaInline]

    def has_add_permission(self, request):
        if request.user.is_admin:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_admin:
            return True
        else:
            return False

    def has_module_permission(self, request):
        if request.user.is_admin:
            return True
        else:
            return False


# Register your models here.
admin.site.register(SportType, SportTypeAdmin)