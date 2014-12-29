# coding: utf-8

from datetime import (
    datetime,
    timedelta,
)
import json
import numbers

from django.contrib.auth.models import User
from django.test import TestCase
from pytz import UTC

from app.routes.models import Route
from app.routes.tests.tests import TestRoutesTestCase
from .models import (
    BestTime,
    Distance,
    Sport,
    Workout,
)
from .views.api import _get_chart_data_from_track


class CreateWorkoutsMixin(object):
    fixtures = ['init_data']

    def setUp(self):
        # create request and user
        self.user = User.objects.create(
            username='a', email='a@a.aa', password='a')

        # create workout
        sport = Sport.objects.create(name=u'sport', category='cycling')
        defaults = {
            'user': self.user,
            'sport': sport,
            'datetime_start': datetime(2000, 01, 01, 12, tzinfo=UTC),
            'datetime_stop': datetime(2000, 01, 01, 13, tzinfo=UTC),
        }
        self.workout1 = Workout.objects.create(distance=5, **defaults)
        self.workout2 = Workout.objects.create(distance=10.5, **defaults)
        self.workout3 = Workout.objects.create(distance=11.111, **defaults)


class WorkoutTestCase(CreateWorkoutsMixin, TestCase):

    def test_best_time_for_x_km(self):
        test_values = [
            (self.workout1, [
                # (distance, expected_value)
                (1, timedelta(minutes=12)),
                (1.76, timedelta(seconds=1267)),
                (3, timedelta(seconds=2160)),
                (5, timedelta(minutes=60)),
                (8.83, None),
                (10, None),
            ]),
            (self.workout2, [
                (1, timedelta(seconds=342)),
                (1.76, timedelta(seconds=603)),
                (3, timedelta(seconds=1028)),
                (5, timedelta(seconds=1714)),
                (8.83, timedelta(seconds=3027)),
                (10, timedelta(seconds=3428)),
            ]),
            (self.workout3, [
                (1, timedelta(seconds=324)),
                (1.76, timedelta(seconds=570)),
                (3, timedelta(seconds=972)),
                (5, timedelta(seconds=1620)),
                (8.83, timedelta(seconds=2860)),
                (10, timedelta(seconds=3240)),
            ]),
        ]

        for workout, test_cases in test_values:
            for case in test_cases:
                self.assertEqual(workout.best_time_for_x_km(case[0]), case[1])

    def test_workout_without_route_track_property_returns_none(self):
        self.assertIsNone(self.workout1.track)

    def test_workout_with_empty_route_track_property_returns_none(self):
        route = Route(workout=self.workout1, user=self.user, tracks_json='[]')
        self.workout1.routes.add(route)
        self.assertIsNone(self.workout1.track)

    def test_workout_with_route_track_property_returns_route(self):
        track_json = """
            [{"segments": [[{
                "lat": 52.263643755, "time": "2013-09-08 10:15:04",
                "lon": 21.162123266, "ele": 86.9
            },{
                "lat": 52.263777986, "time": "2013-09-08 10:15:19",
                "lon": 21.162024105, "ele": 86.4}
            ]]}]
        """
        expected_track_json = {
            'segments': [[{
                    'lat': 52.263643755,
                    'time': '2013-09-08 10:15:04',
                    'lon': 21.162123266,
                    'ele': 86.9
            }, {
                    'lat': 52.263777986,
                    'time': '2013-09-08 10:15:19',
                    'lon': 21.162024105,
                    'ele': 86.4}
            ]]
        }
        route = Route(
            workout=self.workout1,
            user=self.user,
            tracks_json=track_json
        )
        self.workout1.routes.add(route)
        self.assertEquals(self.workout1.track, expected_track_json)

    def test_workout_without_route_show_chart_property_returns_false(self):
        self.assertFalse(self.workout1.show_chart)

    def test_workout_with_empty_route_show_chart_property_returns_false(self):
        route = Route(workout=self.workout1, user=self.user, tracks_json='[]')
        self.workout1.routes.add(route)
        self.assertFalse(self.workout1.show_chart)

    def test_workout_with_route_show_chart_property_returns_true(self):
        track_json = """
            [{"segments": [[{
                "lat": 52.263643755, "time": "2013-09-08 10:15:04",
                "lon": 21.162123266, "ele": 86.9
            },{
                "lat": 52.263777986, "time": "2013-09-08 10:15:19",
                "lon": 21.162024105, "ele": 86.4}
            ]]}]
        """
        route = Route(
            workout=self.workout1,
            user=self.user,
            tracks_json=track_json
        )
        self.workout1.routes.add(route)
        self.assertTrue(self.workout1.show_chart)

    def test_workout_with_route_wo_time_show_chart_prop_returns_false(self):
        track_json = """
            [{"segments": [[{
                "lat": 52.263643755, "lon": 21.162123266, "ele": 86.9
            },{
                "lat": 52.263777986, "lon": 21.162024105, "ele": 86.4}
            ]]}]
        """
        route = Route(
            workout=self.workout1,
            user=self.user,
            tracks_json=track_json
        )
        self.workout1.routes.add(route)
        self.assertFalse(self.workout1.show_chart)

class BestTimesTestCase(CreateWorkoutsMixin, TestCase):

    def setUp(self):
        super(BestTimesTestCase, self).setUp()
        self.distance1 = Distance.objects.get(distance=1)
        self.distance3 = Distance.objects.get(distance=3)
        self.distance4 = Distance.objects.get(distance=5)
        self.distance6 = Distance.objects.get(distance=10)

    def test_best_times_creation(self):
        test_values = [
            (self.workout1, [
                # (distance, expected_value)
                (1, timedelta(minutes=12)),
                (3, timedelta(seconds=2160)),
                (5, timedelta(minutes=60)),
            ]),
            (self.workout2, [
                (1, timedelta(seconds=342)),
                (3, timedelta(seconds=1028)),
                (5, timedelta(seconds=1714)),
                (10, timedelta(seconds=3428)),
            ]),
            (self.workout3, [
                (1, timedelta(seconds=324)),
                (3, timedelta(seconds=972)),
                (5, timedelta(seconds=1620)),
                (10, timedelta(seconds=3240)),
            ]),
        ]

        for workout, test_cases in test_values:
            for case in test_cases:
                distance = Distance.objects.get(distance=case[0])
                best_time = BestTime.objects.get(
                    workout=workout, distance=distance)
                self.assertEqual(best_time.duration, case[1])

    def test_best_times_update(self):
        distance = Distance.objects.get(distance=5)
        best_time = \
            BestTime.objects.get(workout=self.workout1, distance=distance)
        self.assertEqual(best_time.duration, timedelta(minutes=60))

        # update workout and check best time
        self.workout1.datetime_stop = datetime(2000, 01, 01, 14, tzinfo=UTC)
        self.workout1.save()
        best_time = \
            BestTime.objects.get(workout=self.workout1, distance=distance)
        self.assertEqual(best_time.duration, timedelta(minutes=120))


class SportTestCase(TestCase):
    fixtures = ['init_data']

    def setUp(self):
        self.running = Sport.objects.get(id=47)
        self.bowling = Sport.objects.get(id=48)
        self.cycling = Sport.objects.get(id=8)

    def test_get_sports_choices(self):
        choices = Sport.get_sports_choices()

        # ensure choices are list
        self.assertIsInstance(choices, list)

        for index, choice in enumerate(choices):
            # ensure every choice is two elements tuple
            self.assertIsInstance(choice, tuple)
            self.assertEquals(len(choice), 2)

            if index == 0:
                # ensure first choice is no choice
                self.assertEquals(choice[0], '')
            else:
                # ensure firts tuple item is id, second is unicode
                self.assertIsInstance(choice[0], numbers.Integral)
                self.assertIsInstance(choice[1], unicode)

    def test_get_distances_metric_running(self):
        distance_ids = [d.id for d in self.running.get_distances()]
        expected_ids = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(distance_ids, expected_ids)

    def test_get_distances_metric_cycling(self):
        distance_ids = [d.id for d in self.cycling.get_distances()]
        expected_ids = [1, 2, 3, 4, 7, 8]
        self.assertListEqual(distance_ids, expected_ids)

    def test_get_distances_metric_bowling(self):
        self.assertIsNone(self.bowling.get_distances())


class WorkoutChartTestCase(TestRoutesTestCase):
    def test_get_kmph_on_km_pace_data_from_track_returns_right_lenght(self):
        track = json.loads(self.route.tracks_json)[0]
        data = _get_chart_data_from_track(track)
        self.assertEquals(len(data), 4)
        self.assertEquals(len(data[0]), 196)
        self.assertEquals(len(data[1]), 196)
        self.assertEquals(len(data[2]), 196)
        self.assertEquals(len(data[3]), 196)

    def test_get_kmph_on_km_pace_data_from_track_returns_right_data(self):
        track = json.loads(self.route.tracks_json)[0]
        data = _get_chart_data_from_track(track)

        pace_x = data[0]
        pace_y = data[1]
        altitude_x = data[2]
        altitude_y = data[3]

        self.assertEquals(pace_x[0], 'pace-x')
        self.assertEquals(pace_y[0], 'pace-y')
        self.assertEquals(pace_x[1], 0.095)
        self.assertEquals(pace_y[1], 9.76)
        self.assertEquals(pace_x[70], 4.547)
        self.assertEquals(pace_y[70], 6.82)
        self.assertEquals(pace_x[-1], 14.451)
        self.assertEquals(pace_y[-1], 8.39)

        self.assertEquals(altitude_x[0], 'altitude-x')
        self.assertEquals(altitude_y[0], 'altitude-y')
        self.assertEquals(altitude_x[1], 0.095)
        self.assertEquals(altitude_y[1], 93.7)
        self.assertEquals(altitude_x[70], 4.547)
        self.assertEquals(altitude_y[70], 89)
        self.assertEquals(altitude_x[-1], 14.451)
        self.assertEquals(altitude_y[-1], 87.5)
