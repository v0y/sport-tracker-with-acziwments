# coding: utf-8

from datetime import datetime

from django.contrib.auth.models import User
from django_nose import FastFixtureTestCase

from app.health.models import Health
from .enums import SEX_SELECT
from .helpers import get_mail_provider_url


class TestGetMailProvider(FastFixtureTestCase):

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


class UserProfileTestCase(FastFixtureTestCase):

    def setUp(self):
        # helpers vars
        self.date1 = datetime.strptime('01 01 2013', '%d %m %Y')
        self.date2 = datetime.strptime('02 01 2013', '%d %m %Y')
        self.date3 = datetime.strptime('03 01 2013', '%d %m %Y')

        # create users
        self.u1 = User.objects.create_user('u1', 'u1@example.com', 'qwerty')
        self.u2 = User.objects.create_user('u2', 'u2@example.com', 'qwerty')
        self.u3 = User.objects.create_user('u3', 'u3@example.com', 'qwerty')
        self.u4 = User.objects.create_user('u4', 'u4@example.com', 'qwerty')

        # set health
        self.u1.health.add(Health(related_date=self.date1, weight=100))
        self.u2.health.add(
            Health(related_date=self.date1, weight=56.9, fat=4., water=1.5))
        self.u2.health.add(Health(related_date=self.date2, fat=43, water=1.9))
        self.u2.health.add(Health(related_date=self.date3, water=1))
        self.u4.health.add(
            Health(related_date=self.date2, weight=98., fat=69., water=13.))

        # set height
        self.u1.profile.height = 150
        self.u2.profile.height = 170
        self.u3.profile.height = 240

        # set sex
        self.u1.profile.sex = SEX_SELECT[0][0]
        self.u2.profile.sex = SEX_SELECT[0][0]
        self.u3.profile.sex = SEX_SELECT[1][0]
        self.u4.profile.sex = SEX_SELECT[1][0]


class TestUserProfile(UserProfileTestCase):

    def test_bmi(self):
        self.assertEqual(self.u1.profile.bmi, (44.44, self.date1.date()))
        self.assertEqual(self.u2.profile.bmi, (19.69, self.date1.date()))
        self.assertEqual(self.u3.profile.bmi, None)
        self.assertEqual(self.u4.profile.bmi, None)

    def test_sex_visible(self):
        self.assertEqual(self.u1.profile.sex_visible, SEX_SELECT[0][1])
        self.assertEqual(self.u2.profile.sex_visible, SEX_SELECT[0][1])
        self.assertEqual(self.u3.profile.sex_visible, SEX_SELECT[1][1])
        self.assertEqual(self.u4.profile.sex_visible, SEX_SELECT[1][1])

    def test_last_weight(self):
        self.assertEqual(self.u1.profile.last_weight, (100, self.date1.date()))
        self.assertEqual(
            self.u2.profile.last_weight, (56.9, self.date1.date()))
        self.assertEqual(self.u3.profile.last_weight, None)
        self.assertEqual(self.u4.profile.last_weight, (98, self.date2.date()),)

