# encoding: utf-8

from django.contrib import admin

from .models import Health


class HealthAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'fat', 'water', 'related_date')
admin.site.register(Health, HealthAdmin)
