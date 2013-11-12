# encoding: utf-8

from django.contrib import admin

from .models import Sport, Workout


class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
admin.site.register(Sport, SportAdmin)


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'sport', 'distance')
admin.site.register(Workout, WorkoutAdmin)
