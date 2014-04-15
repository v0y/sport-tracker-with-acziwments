# encoding: utf-8

from datetime import datetime
from pytz import UTC

from django.conf import settings
from django.contrib.sites.models import Site
from django_nose import FastFixtureTestCase

from .helpers import unix_time
from .models import SHA1TokenMixin


class SHA1TokenMixinTestCase(FastFixtureTestCase):
    urls = 'app.test_urls'

    def setUp(self):
        self.token = SHA1TokenMixin(token='123')

    def test_get_activation_link(self):
        domain = Site.objects.get(pk=settings.SITE_ID).domain

        link1 = self.token.get_activation_link('test1')
        link2 = self.token.get_activation_link('test1', 'ticket')

        self.assertEqual(link1, 'http://%s/test1?token=123' % domain)
        self.assertEqual(link2, 'http://%s/test1?ticket=123' % domain)


class HelpersTestCase(FastFixtureTestCase):

    def test_unix_time_is_not_aware(self):
        test_datetime = datetime(2010, 1, 2, 3, 4, 5)
        self.assertEquals(unix_time(test_datetime), 1262401445)

    def test_unix_time_is_aware(self):
        test_datetime = datetime(2010, 1, 2, 3, 4, 5, tzinfo=UTC)
        self.assertEquals(unix_time(test_datetime), 1262401445)
