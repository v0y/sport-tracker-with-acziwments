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

    def test_get_datas(self):
        u1_datas = Health.get_datas(self.u1, 'year', '2013')
        u2_datas = Health.get_datas(self.u2, 'week', '2013-01-02')
        u3_datas = Health.get_datas(self.u3, 'month', '2013-01')
        u4_datas = Health.get_datas(self.u4, 'month', '2013-01')

        u1_expected_datas = {
            'weight': [{'x': '2013-01-01', 'y': 100}],
            'fat': [{'x': '2013-01-01', 'y': None}],
            'water': [{'x': '2013-01-01', 'y': None}]
        }
        u2_expected_datas = {
            'weight': [
                {'x': '2013-01-02', 'y': None},
                {'x': '2013-01-03', 'y': None}
            ],
            'fat': [
                {'x': '2013-01-02', 'y': 43},
                {'x': '2013-01-03', 'y': None}
            ],
            'water': [
                {'x': '2013-01-02', 'y': 1.9},
                {'x': '2013-01-03', 'y': 1}
            ]
        }
        u3_expected_datas = {'weight': [], 'fat': [], 'water': []}
        u4_expected_datas = {
            'weight': [{'x': '2013-01-02', 'y': 98}],
            'fat': [{'x': '2013-01-02', 'y': 69}],
            'water': [{'x': '2013-01-02', 'y': 13}]
        }

        self.assertEqual(u1_datas, u1_expected_datas)
        self.assertEqual(u2_datas, u2_expected_datas)
        self.assertEqual(u3_datas, u3_expected_datas)
        self.assertEqual(u4_datas, u4_expected_datas)
