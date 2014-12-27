# encoding: utf-8

from django.contrib import admin

from .models import (
    Activity,
    ActivityType,
)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'type')
admin.site.register(Activity, ActivityAdmin)


class ActivityTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(ActivityType, ActivityTypeAdmin)

