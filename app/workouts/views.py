# coding: utf-8

import datetime
import json
import re

from annoying.decorators import ajax_request
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import CreateView

from app.routes.gpx_handler import get_points_distance_and_elevation
from app.routes.helpers import get_distance, handle_datetime_string
from app.shared.views import LoginRequiredMixin
from .forms import WorkoutForm
from .models import Workout


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = WorkoutForm

    def form_valid(self, form):
        post = self.request.POST

        # change time format to HH:MM:SS and split
        time_start_split = re.sub('[.,]', ':', post['time_start']).split(':')

        # get hour, minute and second of start time
        hour = int(time_start_split[0])
        minute = int(time_start_split[1])
        second = int(time_start_split[2]) if len(time_start_split) >= 3 else 0

        # get duration of workout
        duration = datetime.timedelta(
            hours=int(post['duration_hours'] or 0),
            minutes=int(post['duration_mins'] or 0),
            seconds=int(post['duration_secs'] or 0))

        # update fields
        form.instance.datetime_start = form.instance.datetime_start \
            .replace(hour=hour, minute=minute, second=second)
        form.instance.datetime_stop = form.instance.datetime_start + duration
        form.instance.user_id = self.request.user.id

        return super(WorkoutCreateView, self).form_valid(form)


class LastWorkoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            latest_pk = Workout.objects.filter(user=request.user) \
                .latest('datetime_start').pk
        except Workout.DoesNotExist:
            return render(request, 'workouts/workout_missing.html')

        return redirect('workout_show', latest_pk)


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
    track = json.loads(workout.routes.first().tracks_json)[0]

    return _get_chart_data_from_track(track)

