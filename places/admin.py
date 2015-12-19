from django.contrib import admin
from .models import Place, City, Region, Country


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


admin.site.register(City)
admin.site.register(Country, CountryAdmin)
admin.site.register(Place, PlaceAdmin)