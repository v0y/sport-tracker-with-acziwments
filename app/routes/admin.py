# encoding: utf-8

from django.contrib import admin

from .models import Route


class RoutesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Route, RoutesAdmin)
