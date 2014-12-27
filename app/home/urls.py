# coding: utf-8

from django.conf.urls import (
    patterns,
    url,
)
from django.views.generic import TemplateView

urlpatterns = patterns('app.home.views',
    url(r'^$',
        TemplateView.as_view(template_name='home/homepage.html'),
        name="home")
)
