# coding: utf-8

from django.views.generic.edit import CreateView

from .forms import WorkoutForm
from .models import Workout


class WorkoutCreate(CreateView):
    model = Workout
    form_class = WorkoutForm
