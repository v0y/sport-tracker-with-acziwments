# coding: utf-8

import json

from annoying.decorators import ajax_request
from django.http import HttpResponse
from django.shortcuts import (
    get_object_or_404,
)

from app.routes.gpx_handler import get_points_distance_and_elevation
from app.routes.helpers import (
    get_distance,
    handle_datetime_string,
)
from ..models import Workout


def workouts_calendar_api(request):
    """
    Get all workouts and return as json for calendar.
    """

    events = []
    current_workout_pk = request.POST.get('current_workout_pk')

    for workout in Workout.objects.all():
        # make title string
        title = workout.sport.name
        if workout.distance:
            title += ', %s km' % workout.distance

        # make workout dict
        workout_dict = {
            'title': title,
            'start': workout.datetime_start.isoformat(),
            'url': workout.get_absolute_url()
        }

        # color current workout, remove url, set current month and year
        if int(current_workout_pk) == workout.pk:
            workout_dict['color'] = '#f18d05'  # styles in python xD
            workout_dict.pop('url')

        # append workout dict to workouts list
        events.append(workout_dict)

    return HttpResponse(
        json.dumps(events), content_type="application/json")


def _get_chart_data_from_track(track):
    """
    [
        ['pace-y', (...)]
        ['pace-x', (...)]
        ['altitude-y', (...)]
        ['altitude-x', (...)]
    ]
    """
    for segment in track['segments']:
        i = 1
        pace_y = ['pace-y']
        pace_x = ['pace-x']
        altitude_y = ['altitude-y']
        altitude_x = ['altitude-x']
        while i < len(segment):
            point1 = segment[i - 1]
            point2 = segment[i]
            points_distance = get_distance(point1, point2)
            time1 = handle_datetime_string(point1['time'])
            time2 = handle_datetime_string(point2['time'])
            points_timedelta = time2 - time1
            pace = points_distance / (points_timedelta.seconds / 3600.)
            distance = get_points_distance_and_elevation(segment[0:i + 1])[0]

            pace_y.append(round(pace, 2))
            pace_x.append(round(distance, 3))
            altitude_y.append(round(point2['ele'], 2))
            altitude_x.append(round(distance, 3))
            i += 1

        return [pace_x, pace_y, altitude_x, altitude_y]


@ajax_request
def workout_chart_api(request):
    """
    Get data for workout chart
    """
    workout_id = request.POST['workout_id']
    workout = get_object_or_404(Workout, id=workout_id)
    return _get_chart_data_from_track(workout.track)
