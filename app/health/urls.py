# encoding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('app.health.views',
    url(r'^/add$', 'add_health', name='add_health'),
    url(r'^/edit/(?P<pk>[0-9]+)$', 'edit_health', name='edit_health'),
    # charts
    url(r'^/show/charts$', 'health_show_charts', name='health_show_charts'),
    url(r'^/show/charts/(?P<username>[\w.@+-]+)$',
        'health_show_charts', name='health_show_charts'),
    url(r'^/show/charts/(?P<username>[\w.@+-]+)/'
        r'(?P<range_type>week|month|year)/'
        r'(?P<date>(\d{4})(-\d{2})?(-\d{2})?)$',
        'health_show_charts', name='health_show_charts'),
    # list
    url(r'^/show/list$', 'health_show_list', name='health_show_list'),
    url(r'^/show/list/(?P<username>[\w.@+-]+)$',
        'health_show_list', name='health_show_list'),
    # api
    url('^/api$', 'health_api', name='health_api'),
)
