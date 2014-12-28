# coding: utf-8

import datetime
import re

from django.shortcuts import (
    redirect,
    render,
)
from django.views.generic import View
from django.views.generic.edit import CreateView

from app.shared.views import LoginRequiredMixin
from ..forms import WorkoutForm
from ..models import Workout


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
