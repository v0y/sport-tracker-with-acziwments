# coding: utf-8

from django.conf.urls import (
    include,
    patterns,
    url,
)
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    # admin
    url(r'^admin/doc', include('django.contrib.admindocs.urls')),
    url(r'^admin', include(admin.site.urls)),

    # api
    (r'^api', include('app.urls.api')),

    # home
    url(r'^', include('app.home.urls')),

    # accounts
    (r'^accounts', include('app.accounts.urls')),

    # health
    (r'^health', include('app.health.urls')),

    # workouts
    (r'^workouts', include('app.workouts.urls.urls', namespace='workouts')),
)
