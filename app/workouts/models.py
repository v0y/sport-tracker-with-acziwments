# encoding: utf-8

from django.contrib.auth.models import User
from django.db import models

from app.shared.models import CreatedAtMixin, NameMixin, SlugMixin


class Sport(NameMixin, SlugMixin):
    pass


class Workout(CreatedAtMixin, NameMixin):
    user = models.ForeignKey(
        User, verbose_name=u'Użytkownik', related_name='workouts')
    sport = models.ForeignKey('Sport', verbose_name=u'Duscyplina')
    notes = models.CharField(verbose_name=u"Notatki", max_length=512)
    distance = models.FloatField(verbose_name=u"Dystans w km")
    datetime_start = models.DateTimeField(verbose_name=u"Czas rozpoczęcia")
    datetime_stop = models.DateTimeField(verbose_name=u"Czas zakończenia")

    @property
    def duration(self):
        return self.datetime_stop - self.datetime_start
