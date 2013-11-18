# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # admin
    url(r'^admin/doc', include('django.contrib.admindocs.urls')),
    url(r'^admin', include(admin.site.urls)),
    # home
    url(r'^', include('app.home.urls')),
    # accounts
    (r'^accounts', include('app.accounts.urls')),
    # health
    (r'^health', include('app.health.urls')),
    # routes
    (r'^routes', include('app.routes.urls')),

)
