# encoding: utf-8

from django.conf.urls import patterns, url

from .views import WorkoutCreate


urlpatterns = patterns('',
    url(r'^/add$', WorkoutCreate.as_view(), name='workout_add'),
)
