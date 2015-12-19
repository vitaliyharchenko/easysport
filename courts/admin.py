from django.contrib import admin
from .models import Court, CourtType
from utils import permissions


class CourtAdmin(admin.ModelAdmin):
    model = Court
    fields = (
        'title', 'description', 'photo', 'admin_description', 'place', 'type', 'sporttypes', 'phone', 'max_players', 'cost')

    def has_add_permission(self, request):
        return permissions.only_admin_permissions(request)

    def has_change_permission(self, request, obj=None):
        return permissions.only_admin_permissions(request)

    def has_module_permission(self, request):
        return permissions.only_admin_permissions(request)

# Register your models here.
admin.site.register(CourtType)
admin.site.register(Court, CourtAdmin)