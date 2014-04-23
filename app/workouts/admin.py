# encoding: utf-8

from django.contrib import admin

from .models import BestTime, Distance, Sport, Workout


class BestTimeAdmin(admin.ModelAdmin):
    list_display = ('distance', 'workout', 'unit', 'duration', 'user')
admin.site.register(BestTime, BestTimeAdmin)


class DistanceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'distance', 'unit')
admin.site.register(Distance, DistanceAdmin)


class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
admin.site.register(Sport, SportAdmin)


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'sport', 'distance')
admin.site.register(Workout, WorkoutAdmin)
