from django.contrib import admin
from .models import Court, CourtType


class CourtAdmin(admin.ModelAdmin):
    model = Court
    fields = (
        'title', 'description', 'photo', 'admin_description', 'place', 'type', 'phone', 'max_players', 'cost')

# Register your models here.
admin.site.register(CourtType)
admin.site.register(Court, CourtAdmin)