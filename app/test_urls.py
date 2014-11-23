# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

# TODO: ja pierdolę, co to za gówno?
urlpatterns = patterns('',
    url(r'^test1', RedirectView.as_view(url='http://google.pl'), name='test1'),
)
