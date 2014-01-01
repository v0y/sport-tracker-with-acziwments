# encoding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('app.routes.api_views',
    url(r'^/api/upload_gpx$', 'upload_gpx', name='upload_gpx'),
    url(r'^/api/get_route_json$', 'get_route_json', name='get_route_json'),
)
