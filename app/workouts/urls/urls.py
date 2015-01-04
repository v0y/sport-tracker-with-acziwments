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
    WorkoutChartsView,
)


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/workouts/show')),
    url(r'^/show$', LastWorkoutView.as_view(), name='show_last'),
    url(r'^/show/(?P<pk>\d+)$',
        DetailView.as_view(model=Workout), name='show'),
    url(r'^/add$', WorkoutCreateView.as_view(), name='add'),
    # charts
    url(r'^/show/charts$', WorkoutChartsView.as_view(), name='show_charts'),
    url(r'^/show/charts/(?P<username>[\w.@+-]+)$',
        WorkoutChartsView.as_view(), name='show_charts'),
    url(r'^/show/charts/(?P<username>[\w.@+-]+)/'
        r'(?P<data_type>distance|time|personal-best)/'
        r'(?P<range_type>week|month|year)/'
        r'(?P<date>(\d{4})(-\d{2})?(-\d{2})?)$',
        WorkoutChartsView.as_view(), name='show_charts'),
    url(r'^/show/charts/(?P<username>[\w.@+-]+)/'
        r'(?P<data_type>distance|time|personal-best)/'
        r'(?P<range_type>all-time)$',
        WorkoutChartsView.as_view(), name='show_charts'),
)
