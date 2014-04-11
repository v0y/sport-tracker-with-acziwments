# coding: utf-8

from datetime import datetime, timedelta
from os.path import dirname, join, realpath
from pytz import UTC

from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django_nose import FastFixtureTestCase

from ..gpx_handler import handle_gpx
from ..models import Route


_current_dir = dirname(realpath(__file__))


class TestRoutesTestCase(FastFixtureTestCase):

    def setUp(self):
        # get gpx
        gpx_file = open(join(_current_dir, 'test.gpx'), 'r')
        self.gpx_data = handle_gpx(gpx_file, round_distance_to=3)

        # create request and user
        factory = RequestFactory()
        user = User.objects.create(username='a', email='a@a.aa', password='a')
        self.request = factory.get('/')
        self.request.user = user

        # create route
        gpx_file = open(join(_current_dir, 'test.gpx'), 'r')
        route_id, _ = Route.route_from_gpx(gpx_file, self.request)
        self.route = Route.objects.get(id=route_id)

    def test_handle_gpx(self):
        tracks, start_time, finish_time, length, height_up, height_down = \
            self.gpx_data

        # test basic data from gpx route
        expected_start_time = datetime(2014, 3, 3, 18, 37, 26, tzinfo=UTC)
        expected_finish_time = datetime(2014, 3, 3, 20, 22, 36, tzinfo=UTC)

        self.assertEquals(start_time, expected_start_time)
        self.assertEquals(finish_time, expected_finish_time)
        self.assertAlmostEquals(length, 14.451, delta=0.001)
        self.assertAlmostEquals(height_up, 45.8, delta=0.01)
        self.assertAlmostEquals(height_down, -52.2, delta=0.01)

        # test track
        track = tracks[0]
        segments = track['segments']
        segment = segments[0]

        self.assertEquals(len(tracks), 1)
        self.assertEquals(len(segments), 1)
        self.assertEquals(len(segment), 196)

        last_point_time = None
        for i, point in enumerate(segment):
            self.assertTrue(point['lat'])
            self.assertTrue(point['lon'])
            self.assertTrue(point['ele'])
            self.assertTrue(point['time'])

            # test if points are in correct order
            if not i == 0:
                self.assertTrue(last_point_time < point['time'])
            last_point_time = point['time']

    def test_best_time_for_x_km(self):
        time_for_1_km = self.route.best_time_for_x_km(1)
        time_for_1_76_km = self.route.best_time_for_x_km(1.76)
        time_for_3_km = self.route.best_time_for_x_km(3)
        time_for_5_km = self.route.best_time_for_x_km(5)
        time_for_8_38_km = self.route.best_time_for_x_km(8.38)
        time_for_10_km = self.route.best_time_for_x_km(10)
        time_for_1000_km = self.route.best_time_for_x_km(1000)

        expected_for_1_km = timedelta(minutes=5, seconds=43)
        expected_for_1_76_km = timedelta(minutes=12, seconds=2)
        expected_for_3_km = timedelta(minutes=20, seconds=50)
        expected_for_5_km = timedelta(minutes=35, seconds=13)
        expected_for_8_38_km = timedelta(hours=1, seconds=5)
        expected_for_10_km = timedelta(hours=1, minutes=11, seconds=56)

        self.assertEqual(time_for_1_km, expected_for_1_km)
        self.assertEqual(time_for_1_76_km, expected_for_1_76_km)
        self.assertEqual(time_for_3_km, expected_for_3_km)
        self.assertEqual(time_for_5_km, expected_for_5_km)
        self.assertEqual(time_for_8_38_km, expected_for_8_38_km)
        self.assertEqual(time_for_10_km, expected_for_10_km)
        self.assertEqual(time_for_1000_km, None)

    def test_best_time_for_x_mi(self):
        time_for_1_mi = self.route.best_time_for_x_mi(1)
        time_for_3_mi = self.route.best_time_for_x_mi(3)

        expected_for_1_mi = timedelta(minutes=9, seconds=52)
        expected_for_3_mi = timedelta(minutes=34)

        self.assertEqual(time_for_1_mi, expected_for_1_mi)
        self.assertEqual(time_for_3_mi, expected_for_3_mi)
