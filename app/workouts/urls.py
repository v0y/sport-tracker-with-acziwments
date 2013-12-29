# encoding: utf-8

from django.conf.urls import patterns, url
from django.views.generic.detail import DetailView

from .models import Workout
from .views import workouts_calendar_api, WorkoutCreateView


urlpatterns = patterns('',
    url(r'^/add$', WorkoutCreateView.as_view(), name='workout_add'),
    url(r'^/show/(?P<pk>\d+)$',
        DetailView.as_view(model=Workout), name='workout_show'),
    
    # api
    url(r'^/api/get/all$', workouts_calendar_api, name='workouts_calendar_api')
)
