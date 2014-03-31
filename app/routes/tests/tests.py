# coding: utf-8

from datetime import datetime
from os.path import dirname, join, realpath
from pytz import UTC

from django_nose import FastFixtureTestCase

from ..gpx_handler import handle_gpx


_current_dir = dirname(realpath(__file__))


class TestRoutesTestCase(FastFixtureTestCase):

    def setUp(self):
        gpx_file = open(join(_current_dir, 'test.gpx'), 'r')
        self.gpx_data = handle_gpx(gpx_file)

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
