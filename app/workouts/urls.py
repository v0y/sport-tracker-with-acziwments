# encoding: utf-8

from django.conf.urls import patterns, url
from django.views.generic.detail import DetailView

from .models import Workout
from .views import WorkoutCreateView


urlpatterns = patterns('',
    url(r'^/add$', WorkoutCreateView.as_view(), name='workout_add'),
    url(r'^/show/detail/(?P<pk>\d+)$',
        DetailView.as_view(model=Workout), name='workout_show'),
)
