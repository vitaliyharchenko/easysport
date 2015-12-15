from django.contrib import admin
from .models import Court, Place, City, Region, Country, CourtType


class RegionInline(admin.TabularInline):
    model = Region
    extra = 0


class CountryAdmin(admin.ModelAdmin):
    model = Country
    inlines = [RegionInline]


class CourtAdmin(admin.ModelAdmin):
    model = Court
    fields = (
        'title', 'description', 'photo', 'admin_description', 'place', 'type', 'phone', 'max_players', 'cost')
    # filter_horizontal = ('sporttypes',)

# Register your models here.
admin.site.register(City)
admin.site.register(Country, CountryAdmin)
admin.site.register(Place)
admin.site.register(CourtType)
admin.site.register(Court, CourtAdmin)