from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserAdmin(UserAdmin):
    list_display = ('email', 'name', 'date_joined',)
    search_fields = ('email', 'name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    ordering = ('email',)
    list_filter = ()
    fieldsets = ()


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'blood_group')
    search_fields = ('user', 'gender', 'blood_group',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ('gender', 'blood_group',)


admin.site.register(User, UserAdmin)
admin.site.register(ProfileModel, ProfileModelAdmin)
