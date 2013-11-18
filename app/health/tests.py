# encoding: utf-8

from app.accounts.tests import UserProfileTestCase

from app.health.models import Health


class TestHealth(UserProfileTestCase):

    def test_get_first_date(self):
        u1_first_date = Health.get_first_date(self.u1, '%Y %m %d')
        u2_first_date = Health.get_first_date(self.u2, '%Y %m %d')
        u3_first_date = Health.get_first_date(self.u3, '%Y %m %d')
        u4_first_date = Health.get_first_date(self.u4, '%Y %m %d')

        self.assertEqual(u1_first_date, '2013 01 01')
        self.assertEqual(u2_first_date, '2013 01 01')
        self.assertEqual(u3_first_date, None)
        self.assertEqual(u4_first_date, '2013 01 02')

