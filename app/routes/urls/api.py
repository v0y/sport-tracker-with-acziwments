# encoding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('app.routes.views.api',
    url(r'^upload_gpx$', 'upload_gpx', name='upload_gpx'),
    url(r'^save_route$', 'save_route', name='save_route'),
    url(r'^get_route_json$', 'get_route_json', name='get_route_json'),
)
