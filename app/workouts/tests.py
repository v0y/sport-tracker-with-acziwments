# coding: utf-8

from datetime import datetime, timedelta
import json
import numbers
from pytz import UTC

from django.contrib.auth.models import User
from django.test import TestCase

from app.routes.tests.tests import TestRoutesTestCase
from .models import Distance, Sport, Workout, BestTime
from .views import _get_chart_data_from_track


class CreateWorkoutsMixin(object):
    fixtures = ['init_data']

    def setUp(self):
        # create request and user
        user = User.objects.create(username='a', email='a@a.aa', password='a')

        # create workout
        sport = Sport.objects.create(name=u'sport', category='cycling')
        defaults = {
            'user': user,
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

    def test_best_time_for_x_mi(self):
        time_for_1_mi = self.workout1.best_time_for_x_mi(1)
        time_for_3_mi = self.workout1.best_time_for_x_mi(3)

        expected_for_1_mi = timedelta(seconds=1158)
        expected_for_3_mi = timedelta(seconds=3476)

        self.assertEqual(time_for_1_mi, expected_for_1_mi)
        self.assertEqual(time_for_3_mi, expected_for_3_mi)


class DistancesTestCase(TestCase):
    fixtures = ['init_data']

    def setUp(self):
        self.distance1 = Distance.objects.get(distance=1, unit='km')
        self.distance2 = Distance.objects.get(distance=10, unit='km')
        self.distance3 = Distance.objects.get(distance=42.195, unit='km')
        self.distance4 = Distance.objects.get(distance=1, unit='mi')
        self.distance5 = Distance.objects.create(distance=15.99, unit='mi')
        self.distance6 = Distance.objects.get(distance=100, unit='mi')

    def test_distance_km(self):
        self.assertEqual(self.distance1.distance_km, 1)
        self.assertEqual(self.distance2.distance_km, 10)
        self.assertEqual(self.distance3.distance_km, 42.195)
        self.assertEqual(self.distance4.distance_km, 1.60934)
        self.assertEqual(self.distance5.distance_km, 25.7333466)
        self.assertEqual(self.distance6.distance_km, 160.934)


class BestTimesTestCase(CreateWorkoutsMixin, TestCase):

    def setUp(self):
        super(BestTimesTestCase, self).setUp()
        self.distance1 = Distance.objects.get(distance=1, unit='km')
        self.distance3 = Distance.objects.get(distance=3, unit='km')
        self.distance4 = Distance.objects.get(distance=5, unit='km')
        self.distance6 = Distance.objects.get(distance=10, unit='km')

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
                distance = Distance.objects.get(distance=case[0], unit='km')
                best_time = BestTime.objects.get(
                    workout=workout, distance=distance)
                self.assertEqual(best_time.duration, case[1])

    def test_best_times_update(self):
        distance = Distance.objects.get(distance=5, unit='km')
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
        distance_ids = [d.id for d in self.running.get_distances('km')]
        expected_ids = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(distance_ids, expected_ids)

    def test_get_distances_metric_cycling(self):
        distance_ids = [d.id for d in self.cycling.get_distances('km')]
        expected_ids = [1, 2, 3, 4, 7, 8]
        self.assertListEqual(distance_ids, expected_ids)

    def test_get_distances_metric_bowling(self):
        self.assertIsNone(self.bowling.get_distances('km'))

    def test_get_distances_imperial_running(self):
        distance_ids = [d.id for d in self.running.get_distances('mi')]
        expected_ids = [9, 10, 11, 12, 13, 14, 15, 16]
        self.assertListEqual(distance_ids, expected_ids)

    def test_get_distances_imperial_cycling(self):
        distance_ids = [d.id for d in self.cycling.get_distances('mi')]
        expected_ids = [9, 10, 11, 12, 15, 16]
        self.assertListEqual(distance_ids, expected_ids)

    def test_get_distances_imperial_bowling(self):
        self.assertIsNone(self.bowling.get_distances('mi'))


class WorkoutChartTestCase(TestRoutesTestCase):
    def test_get_kmph_on_km_pace_data_from_track_returns_right_lenght(self):
        track = json.loads(self.route.tracks_json)[0]
        self.assertEquals(
            len(_get_chart_data_from_track(track)['pace']), 195)

    def test_get_kmph_on_km_pace_data_from_track_returns_right_data(self):
        track = json.loads(self.route.tracks_json)[0]
        data = _get_chart_data_from_track(track)

        self.assertEquals(data['pace'][0]['x'], 0.095)
        self.assertEquals(data['pace'][0]['y'], 9.76)
        self.assertEquals(data['pace'][69]['x'], 4.547)
        self.assertEquals(data['pace'][69]['y'], 6.82)
        self.assertEquals(data['pace'][-1]['x'], 14.451)
        self.assertEquals(data['pace'][-1]['y'], 8.39)
