# coding: utf-8

import datetime
import json
import re

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.generic.edit import CreateView

from app.shared.helpers import unix_time
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

    return_json = {
        'events': [],
        'current_month': '',
        'current_year': '',
    }

    current_workout_pk = request.POST.get('current_workout_pk')

    for workout in Workout.objects.all():
        # make title string
        title = workout.sport.name
        if workout.distance:
            title += ', %s km' % workout.distance

        # make workout dict
        workout_dict = {
            'title': title,
            'start': unix_time(workout.datetime_start),
            'url': workout.get_absolute_url()
        }

        # color current workout, remove url, set current month and year
        if int(current_workout_pk) == workout.pk:
            workout_dict['color'] = '#f18d05'  # styles in python xD
            workout_dict.pop('url')
            # we need to subtract 1, 'cause Jan in JS is 0, but in python is 1
            return_json['current_month'] = workout.datetime_start.month - 1
            return_json['current_year'] = workout.datetime_start.year

        # append workout dict to workouts list
        return_json['events'].append(workout_dict)

    return HttpResponse(
        json.dumps(return_json), content_type="application/json")
