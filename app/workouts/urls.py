# encoding: utf-8

from django.conf.urls import patterns, url

from .views import WorkoutCreateView


urlpatterns = patterns('',
    url(r'^/add$', WorkoutCreateView.as_view(), name='workout_add'),
)
