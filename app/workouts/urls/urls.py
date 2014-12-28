# encoding: utf-8

from django.conf.urls import (
    patterns,
    url,
)
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView

from ..models import Workout
from ..views.views import (
    LastWorkoutView,
    WorkoutCreateView,
)


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/workouts/show')),
    url(r'^/show$', LastWorkoutView.as_view(), name='workout_show_last'),
    url(r'^/show/(?P<pk>\d+)$',
        DetailView.as_view(model=Workout), name='workout_show'),
    url(r'^/add$', WorkoutCreateView.as_view(), name='workout_add'),
)
