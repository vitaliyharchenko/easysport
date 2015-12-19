from django.contrib import admin
from .models import Place, City, Region, Country
from utils import permissions


class RegionInline(admin.TabularInline):
    model = Region
    extra = 0


# TODO: name for inline
class CountryAdmin(admin.ModelAdmin):
    model = Country
    inlines = [RegionInline]


class PlaceAdmin(admin.ModelAdmin):
    model = Place
    extra = 0

    def has_add_permission(self, request):
        return permissions.only_admin_permissions(request)

    def has_change_permission(self, request, obj=None):
        return permissions.only_admin_permissions(request)

    def has_module_permission(self, request):
        return permissions.only_admin_permissions(request)


admin.site.register(City)
admin.site.register(Country, CountryAdmin)
admin.site.register(Place, PlaceAdmin)