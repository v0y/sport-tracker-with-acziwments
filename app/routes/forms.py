# encoding: utf-8

from django import forms
from django.forms import Form


class GPXForm(Form):
    gpx_file = forms.FileField()
