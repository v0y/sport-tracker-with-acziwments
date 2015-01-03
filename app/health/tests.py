# encoding: utf-8

from app.accounts.tests import UserProfileTestCase
from app.shared.enums import ChartTimeRange
from .models import Health


class HealthTestCase(UserProfileTestCase):

    def test_get_first_date(self):
        u1_first_date = Health.get_first_date(self.u1, '%Y %m %d')
        u2_first_date = Health.get_first_date(self.u2, '%Y %m %d')
        u3_first_date = Health.get_first_date(self.u3, '%Y %m %d')
        u4_first_date = Health.get_first_date(self.u4, '%Y %m %d')

        self.assertEqual(u1_first_date, '2013 01 01')
        self.assertEqual(u2_first_date, '2013 01 01')
        self.assertEqual(u3_first_date, None)
        self.assertEqual(u4_first_date, '2013 01 02')

    def test_get_data(self):
        u1_data = Health.get_data(self.u1, ChartTimeRange.YEAR, '2013')
        u2_data = Health.get_data(self.u2, ChartTimeRange.WEEK, '2013-01-02')
        u3_data = Health.get_data(self.u3, ChartTimeRange.MONTH, '2013-01')
        u4_data = Health.get_data(self.u4, ChartTimeRange.MONTH, '2013-01')
        u5_data = Health.get_data(self.u4, ChartTimeRange.ALLTIME)

        u1_expected_data = [
            ['fat-y'],
            ['fat-x'],
            ['water-y'],
            ['water-x'],
            ['weight-y', 100],
            ['weight-x', '2013-01-01'],
        ]
        u2_expected_data = [
            ['fat-y', 43],
            ['fat-x', '2013-01-02'],
            ['water-y', 1.9, 1],
            ['water-x', '2013-01-02', '2013-01-03'],
            ['weight-y'],
            ['weight-x'],
        ]
        u3_expected_data = [
            ['fat-y'],
            ['fat-x'],
            ['water-y'],
            ['water-x'],
            ['weight-y'],
            ['weight-x'],
        ]
        u4_expected_data = [
            ['fat-y', 69],
            ['fat-x', '2013-01-02'],
            ['water-y', 13],
            ['water-x', '2013-01-02'],
            ['weight-y', 98],
            ['weight-x', '2013-01-02'],
        ]
        u5_expected_data = u4_expected_data

        self.assertEqual(u1_data, u1_expected_data)
        self.assertEqual(u2_data, u2_expected_data)
        self.assertEqual(u3_data, u3_expected_data)
        self.assertEqual(u4_data, u4_expected_data)
        self.assertEqual(u5_data, u5_expected_data)
