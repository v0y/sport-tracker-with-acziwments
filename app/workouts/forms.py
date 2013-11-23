# encoding: utf-8

from datetime import datetime

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from app.routes.forms import RouteIdMixin
from .models import Workout


class WorkoutForm(RouteIdMixin):
    notes = forms.CharField(
        widget=forms.widgets.Textarea, label=u"Notatki", required=False)
    datetime_start = forms.DateField(label=u"Data", input_formats=['%d-%m-%Y'])
    time_start = forms.TimeField(label=u"Godzina rozpoczęcia")
    duration_hours = forms.IntegerField(
        validators=[MinValueValidator(0)], initial=0, required=False)
    duration_mins = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(59)], initial=0,
        required=False)
    duration_secs = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(59)], initial=0,
        required=False)

    class Meta:
        button_text = u"Zapisz"
        exclude = ('user', 'datetime_stop')
        model = Workout
        name = u"Dodaj trening"

    def __init__(self, initial=None, *args, **kwargs):
        now_ = datetime.now()
        now_date = datetime.strftime(now_, '%d-%m-%Y')
        now_time = datetime.strftime(now_, '%H:%M')

        initial = initial or {}
        initial['datetime_start'] = initial.get('datetime_start', now_date)
        initial['time_start'] = initial.get('time_start', now_time)

        super(WorkoutForm, self).__init__(initial=initial, *args, **kwargs)

    def clean_duration_secs(self):
        cd = self.cleaned_data
        hours = cd.get('duration_hours')
        mins = cd.get('duration_mins')
        secs = cd.get('duration_secs')

        if not any([hours, mins, secs]):
            raise forms.ValidationError(u"Musisz podać czas trwania treningu")

        return secs

    def save(self, *args, **kwargs):
        # save as normal model form
        workout = super(WorkoutForm, self).save(*args, **kwargs)

        # get route and assign it to workout
        self.assign_route_to_workout(workout)

        return workout

