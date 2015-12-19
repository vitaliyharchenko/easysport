from django.contrib import admin
from .models import SportType, GameType, Amplua
from utils import permissions


class GameTypeInline(admin.TabularInline):
    model = GameType
    extra = 0

    def has_add_permission(self, request):
        return permissions.only_admin_permissions(request)

    def has_change_permission(self, request, obj=None):
        return permissions.only_admin_permissions(request)

    def has_module_permission(self, request):
        return permissions.only_admin_permissions(request)


class AmpluaInline(admin.TabularInline):
    model = Amplua
    extra = 0

    def has_add_permission(self, request):
        return permissions.only_admin_permissions(request)

    def has_change_permission(self, request, obj=None):
        return permissions.only_admin_permissions(request)

    def has_module_permission(self, request):
        return permissions.only_admin_permissions(request)


class SportTypeAdmin(admin.ModelAdmin):
    model = SportType
    inlines = [GameTypeInline, AmpluaInline]

    def has_add_permission(self, request):
        return permissions.only_admin_permissions(request)

    def has_change_permission(self, request, obj=None):
        return permissions.only_admin_permissions(request)

    def has_module_permission(self, request):
        return permissions.only_admin_permissions(request)


# Register your models here.
admin.site.register(SportType, SportTypeAdmin)