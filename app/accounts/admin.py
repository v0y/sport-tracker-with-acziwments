# encoding: utf-8

from django.contrib import admin

from .models import EmailActivation, PasswordReset, UserActivation, UserProfile


class EmailActivationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'token', 'created_at')
admin.site.register(EmailActivation, EmailActivationAdmin)


class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
admin.site.register(PasswordReset, PasswordResetAdmin)


class UserActivationAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
admin.site.register(UserActivation, UserActivationAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'sex', 'dob')
admin.site.register(UserProfile, UserProfileAdmin)
