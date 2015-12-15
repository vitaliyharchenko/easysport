from django.db import models
from django.contrib import admin
from .models import Court, CourtType
from utils.fields import JasnyImageWidget, BeautyImageWidget


class CourtAdmin(admin.ModelAdmin):
    model = Court
    fields = (
        'title', 'description', 'photo', 'admin_description', 'place', 'type', 'phone', 'max_players', 'cost')
    formfield_overrides = {
        models.ImageField: {'widget': BeautyImageWidget},
    }

# Register your models here.
admin.site.register(CourtType)
admin.site.register(Court, CourtAdmin)