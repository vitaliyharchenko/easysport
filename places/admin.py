from django.contrib import admin
from .models import Place, City, Region, Country


class RegionInline(admin.TabularInline):
    model = Region
    extra = 0


# TODO: name for inline
class CountryAdmin(admin.ModelAdmin):
    model = Country
    inlines = [RegionInline]


# Register your models here.
admin.site.register(City)
admin.site.register(Country, CountryAdmin)
admin.site.register(Place)