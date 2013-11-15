# encoding: utf-8

from django.contrib.auth.models import User
from django.db import models

from app.shared.models import CreatedAtMixin, NameMixin, SlugMixin
from .enums import SPORT_CATEGORIES


class Sport(NameMixin, SlugMixin):
    category = models.CharField(
        verbose_name=u"Kategoria", choices=SPORT_CATEGORIES, max_length=16)

    class Meta:
        verbose_name = u"sport"
        verbose_name_plural = u"sporty"


class Workout(CreatedAtMixin, NameMixin):
    user = models.ForeignKey(
        User, verbose_name=u"Użytkownik", related_name='workouts')
    sport = models.ForeignKey('Sport', verbose_name=u"Dyscyplina")
    notes = models.CharField(verbose_name=u"Notatki", max_length=512)
    distance = models.FloatField(verbose_name=u"Dystans w km")
    datetime_start = models.DateTimeField(verbose_name=u"Czas rozpoczęcia")
    datetime_stop = models.DateTimeField(verbose_name=u"Czas zakończenia")

    class Meta:
        verbose_name = u"trening"
        verbose_name_plural = u"treningi"

    @property
    def duration(self):
        return self.datetime_stop - self.datetime_start
