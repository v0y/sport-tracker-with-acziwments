# encoding: utf-8

from django.conf.urls import (
    patterns,
    url,
)


urlpatterns = patterns('app.workouts.views.api',
    url(r'^/get/calendar$', 'workouts_calendar_api', name='calendar'),
    url(r'^/get/chart$', 'workout_chart_api', name='chart')
)
