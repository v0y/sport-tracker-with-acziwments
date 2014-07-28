# encoding: utf-8
from datetime import timedelta

import json

from django.contrib.auth.models import User
from django.db import models
from app.routes.gpx_handler import get_distance

from app.shared.helpers import mi2km
from app.shared.models import CreatedAtMixin
from app.workouts.models import Workout
from .gpx_handler import handle_gpx, get_segment_dist_and_ele, \
    get_segment_start_and_finish_times, get_distance_and_elevations_delta


class Route(CreatedAtMixin):
    workout = models.ForeignKey(
        Workout, null=True, related_name=u'routes', default=None,
        verbose_name=u"Trening")
    user = models.ForeignKey(
        User, related_name=u'routes', verbose_name=u"Użytkownik")

    start_time = models.DateTimeField(
        auto_now=False, null=True, verbose_name=u"Czas rozpoczęcia trasy")
    finish_time = models.DateTimeField(
        auto_now=False, null=True, verbose_name=u"Czas zakończenia trasy")
    length = models.FloatField(
        default=0, verbose_name=u"Długość trasy")
    height_up = models.FloatField(
        default=0, verbose_name=u"Różnica wysokości w górę")
    height_down = models.FloatField(
        default=0, verbose_name=u"Różnica wysokości w dół")

    tracks_json = models.TextField(default='[]')

    class Meta:
        verbose_name = u"trasa"
        verbose_name_plural = u"trasy"

    @classmethod
    def route_from_gpx(cls, gpx_file, request):
        tracks, s_time, f_time, length, h_up, h_down = handle_gpx(gpx_file)
        tracks_json = json.dumps(tracks)

        route = cls.objects.create(
            user=request.user,
            start_time=s_time,
            finish_time=f_time,
            length=length,
            height_up=h_up,
            height_down=h_down,
            tracks_json=tracks_json,
        )

        return route.id, tracks_json

    @classmethod
    def save_route(cls, route_data, request):
        tracks_json = json.loads(route_data)
        length, _, _ = get_distance_and_elevations_delta(tracks_json)

        input_dct = {
            'user': request.user,
            'tracks_json': tracks_json,
            'length': length,
        }

        route = cls.objects.create(**input_dct)

        return route.id, route_data


    def best_time_for_x_km(self, distance):
        """
        Get best time on x km

        :param distance: get time for this distance
        :return: fastest time for given distance
        :rtype: timedelta
        """

        if self.length < distance:
            return

        def _get_first_point_over_distance(
                track_, target_distance, old_p1_=None, old_p2_=0):

            start_point = 0 if old_p1_ is None else old_p1_ + 1

            for p2_ in range(start_point, len(track_)):
                # distance would be too short
                if p2_ < old_p2_:
                    continue
                distance_to_p2, _, _ = \
                    get_segment_dist_and_ele(track_[start_point:p2_], 3)
                if distance_to_p2 > target_distance:
                    return p2_

            return None

        def _get_time_for_distance(track_, target_distance, p1_, p2_):
            # get time of track without partial segment
            segment = track_[p1_:p2_ - 1]
            start, finish_partial = get_segment_start_and_finish_times(segment)
            partial_timedelta = finish_partial - start
            distance_partial, _, _ = get_segment_dist_and_ele(segment, 3)

            # get missing distance and its time
            missing_distance = target_distance - distance_partial

            # get last part distance and time
            last_segment = track_[p2_ - 2:p2_]
            start_last, finish_last = \
                get_segment_start_and_finish_times(last_segment)
            last_timedelta = finish_last - start_last
            last_distance = get_distance(track_[p2_ - 2], track_[p2_ - 1])

            # get proportions
            proportions = missing_distance / float(last_distance)

            # get missing time
            missing_seconds = proportions * last_timedelta.seconds
            missing_time = timedelta(seconds=missing_seconds)

            total_time = partial_timedelta + missing_time
            total_time = timedelta(seconds=total_time.seconds)

            return total_time

        times_list = []

        # get first segment of first track in json
        track = json.loads(self.tracks_json)[0]['segments'][0]

        p2 = _get_first_point_over_distance(track, distance)
        old_p2 = p2
        old_p1 = 0

        # get list of times
        while p2 is not None:
            p2 = _get_first_point_over_distance(
                track, distance, old_p1, old_p2)
            if p2 is None:
                break
            times_list.append(
                _get_time_for_distance(track, distance, old_p1 + 1, p2))
            old_p1 += 1
            old_p2 = p2

        return min(times_list)

    def best_time_for_x_mi(self, distance):
        """
        Get best time on x miles

        :param distance: get time for this distance
        :return: fastest time for given distance
        :rtype: timedelta
        """
        return self.best_time_for_x_km(mi2km(distance))
