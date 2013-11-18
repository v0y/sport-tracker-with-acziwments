# encoding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('app.routes.views',
    url(r'^/add$', 'upload_gpx', name='upload_gpx'),
)
