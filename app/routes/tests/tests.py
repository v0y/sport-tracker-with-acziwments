# coding: utf-8

from datetime import datetime, timedelta
import json
from os.path import dirname, join, realpath
from pytz import UTC

from django.contrib.auth.models import User
from django.db import transaction
from django.test import TestCase
from django.test.client import RequestFactory, Client

from ..gpx_handler import handle_gpx
from ..models import Route


_current_dir = dirname(realpath(__file__))


class ManualRouteTestCase(TestCase):
    def setUp(self):
        # needed because:
        # stackoverflow.com/questions/20601499/django-testing-client-log
        transaction.set_autocommit(True)

        # create a user (if it doesn't exist already)...
        if not User.objects.filter(username='b').exists():
            User.objects.create_user(
                username='b', email='b@b.bb', password='b')

        # and a logged in client
        self.client = Client(enforce_csrf_checks=False)
        self.client.login(username='b', password='b')

    def test_stuff(self):
        # prepare some example data
        post_json = json.dumps(
            [
                {'segments':
                    [[
                        {'lat': 13.168149311827042, 'lon': 18.397670779377222},
                        {'lat': 13.156114384691714, 'lon': 18.409343753010035},
                        {'lat': 13.14341020944312, 'lon': 18.425136599689722},
                        {'lat': 13.127361890026977, 'lon': 18.453975711017847},
                        {'lat': 13.124687068167537, 'lon': 18.47938159480691}
                    ]]
                }
            ]
        )
        post_data = {'tracks': post_json}

        # simulate request that POSTs this data
        response = self.client.post(
            '/routes/api/save_route', post_data, follow=True)

        # verify response
        self.assertEqual(response.status_code, 200)
        response_dct = json.loads(response.content)
        self.assertTrue(response_dct['info'], u'OK')

        # check if new route was saved to db...
        route = Route.objects.get(id=response_dct['id'])

        # ...and if it is possible to retrive it from db...
        route_tracks_dct = json.loads(route.tracks_json)
        self.assertTrue('segments' in route_tracks_dct[0])

        # ...and by use of get_route_json view
        response = self.client.get(
            '/routes/api/get_route_json', {'route_id': route.id})
        json.loads(response.content)


class TestRoutesTestCase(TestCase):

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
