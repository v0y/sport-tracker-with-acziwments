# coding: utf-8

from django.conf.urls import (
    patterns,
    include,
)

urlpatterns = patterns('',
    (r'^/routes/', include('app.routes.urls.api')),
)
