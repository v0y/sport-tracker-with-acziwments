# encoding: utf-8

from django.conf.urls import (
    patterns,
    url,
)


urlpatterns = patterns('app.health.views.views',
    url(r'^/add$', 'add_health', name='add'),
    url(r'^/edit/(?P<pk>[0-9]+)$', 'edit_health', name='edit'),
    # charts
    url(r'^/show/charts$', 'health_show_charts', name='show_charts'),
    url(r'^/show/charts/(?P<username>[\w.@+-]+)$',
        'health_show_charts', name='show_charts'),
    url(r'^/show/charts/(?P<username>[\w.@+-]+)/'
        r'(?P<range_type>week|month|year)/'
        r'(?P<date>(\d{4})(-\d{2})?(-\d{2})?)$',
        'health_show_charts', name='show_charts'),
    url(r'^/show/charts/(?P<username>[\w.@+-]+)/(?P<range_type>all-time)$',
        'health_show_charts', name='show_charts'),
    # list
    url(r'^/show/list$', 'health_show_list', name='show_list'),
    url(r'^/show/list/(?P<username>[\w.@+-]+)$',
        'health_show_list', name='show_list'),
)
