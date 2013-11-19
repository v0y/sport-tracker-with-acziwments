# encoding: utf-8

import json

from django.contrib.auth.models import User
from django.db import models

from app.shared.models import CreatedAtMixin
from app.workouts.models import Workout
from .gpx_handler import handle_gpx

class Route(CreatedAtMixin):
    workout = models.ForeignKey(
        Workout, null=True, related_name=u'routes', default=None,
        verbose_name=u"Trening")
    user = models.ForeignKey(
        User, related_name=u'routes', verbose_name=u"Użytkownik")

    start_time = models.DateTimeField(
        auto_now=False, null=True, verbose_name=u'Czas rozpoczęcia trasy')
    finish_time = models.DateTimeField(
        auto_now=False, null=True, verbose_name=u'Czas zakończenia trasy')
    length = models.FloatField(
        default=0, verbose_name=u'Długość trasy')
    height_up = models.FloatField(
        default=0, verbose_name=u'Różnica wysokości w górę')
    height_down = models.FloatField(
        default=0, verbose_name=u'Różnica wysokości w dół')

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
