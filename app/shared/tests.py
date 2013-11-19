# encoding: utf-8

from django.conf import settings
from django.contrib.sites.models import Site
from django_nose import FastFixtureTestCase

from app.shared.models import SHA1TokenMixin


# inherit abstract class
class SHA1Token(SHA1TokenMixin):
    pass


class SHA1TokenMixinTestCase(FastFixtureTestCase):
    urls = 'app.test_urls'

    def setUp(self):
        self.token = SHA1Token(token='123')


class TestSHA1TokenMixin(SHA1TokenMixinTestCase):

    def test_get_activation_link(self):
        domain = Site.objects.get(pk=settings.SITE_ID).domain

        link1 = self.token.get_activation_link('test1')
        link2 = self.token.get_activation_link('test1', 'ticket')

        self.assertEqual(link1, 'http://%s/test1?token=123' % domain)
        self.assertEqual(link2, 'http://%s/test1?ticket=123' % domain)