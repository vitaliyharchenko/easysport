from django.contrib import admin
from .models import Court, CourtType


class CourtAdmin(admin.ModelAdmin):
    model = Court
    fields = (
        'title', 'description', 'photo', 'admin_description', 'place', 'type', 'phone', 'max_players', 'cost')

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
admin.site.register(CourtType)
admin.site.register(Court, CourtAdmin)