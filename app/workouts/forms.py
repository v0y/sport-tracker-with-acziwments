# encoding: utf-8

from django import forms
from django.forms.models import ModelForm

from .models import Workout


class WorkoutForm(ModelForm):
    notes = forms.CharField(
        widget=forms.widgets.Textarea, label=u"Notatki", required=False)

    class Meta:
        button_text = u"Zapisz"
        exclude = ('user',)
        model = Workout
        name = u"Dodaj trening"
