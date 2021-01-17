from django.contrib import admin
from .models import RequestModel


class RequestModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'needed_within',)
    search_fields = ('user',)
    readonly_fields = ('needed_within', 'posted_on')

    filter_horizontal = ()
    ordering = ('-posted_on',)
    fieldsets = ()
    list_filter = ('user', 'blood_group', 'needed_within')


admin.site.register(RequestModel, RequestModelAdmin)
