# encoding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('app.health.views.api',
    url('^/get/chart$', 'health_chart_api', name='chart'),
)
