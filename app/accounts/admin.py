# encoding: utf-8

from django.contrib import admin

from .models import UserActivation


class UserActivationAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')

admin.site.register(UserActivation, UserActivationAdmin)
