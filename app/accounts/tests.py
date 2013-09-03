# coding: utf-8

from unittest import TestCase

from .helpers import get_mail_provider_url


class TestGetMailProvider(TestCase):

    def test_basic(self):
        # {'given mail': 'expected result}
        mails = {
            '': None,
            'lolwut': None,
            'aaa bbb': None,
            'abc@def@lol': None,
            'wp.pl': None,
            '@wp.pl': None,
            'wp.pl@wp.pl@wp.pl': None,
            'mail@spoko.pl': 'http://poczta.onet.pl',
            'dupa.lol.wut.1@gmail.com': 'http://gmail.com',
            'correct_mail@yahoo.com': 'http://login.yahoo.com',
        }

        for mail, result in mails.items():
            self.assertEqual(get_mail_provider_url(mail), result)
