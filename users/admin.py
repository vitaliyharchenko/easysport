from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User, UserActivation
from .forms import UserChangeForm, UserCreationForm
from games.models import UserGameAction
from utils import permissions


class UserGameActionInline(admin.TabularInline):
    model = UserGameAction
    extra = 0

    def has_add_permission(self, request):
        return permissions.admin_organizer_responsible_permissions(request)

    def has_change_permission(self, request):
        return permissions.admin_organizer_responsible_permissions(request)


class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = [UserGameActionInline]

    def has_add_permission(self, request, obj=None):
        return permissions.only_admin_permissions(request)

    def has_change_permission(self, request, obj=None):
        return permissions.only_admin_permissions(request)

    # def has_view_permission(self, request):
    #     return permissions.admin_organizer_responsible_permissions(request)

    def has_module_permission(self, request):
        return permissions.admin_organizer_responsible_permissions(request)

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone')
    list_filter = ('is_active', 'is_responsible', 'is_organizer', 'is_admin', 'is_staff',)
    raw_id_fields = ('referer',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('avatar', 'first_name', 'last_name', 'vkuserid', 'phone',
                                                'referer', 'sex', 'weight', 'height', 'bdate', 'amplua')}),
        ('Доступы', {'fields': ('is_active', 'banned', 'is_referee', 'is_coach', 'is_responsible',
                                'is_organizer', 'is_admin',)}),
    )
    # overrides get_fieldsets to use this attribute when creating a user.
    # add_fieldsets = (
    # (None, {
    # 'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2')}
    #      ),
    # )
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('id',)
    filter_horizontal = ()


class UserActivationAdmin(admin.ModelAdmin):
    model = UserActivation
    readonly_fields = ['user', 'activation_key', 'request_time', 'confirm_time']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


admin.site.register(User, UserAdmin)
admin.site.register(UserActivation, UserActivationAdmin)
admin.site.unregister(Group)