# encoding: utf-8

from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db import models

from app.shared.helpers import mi2km
from app.shared.models import CreatedAtMixin, NameMixin, SlugMixin
from .enums import SPORT_CATEGORIES


class Sport(NameMixin, SlugMixin):
    category = models.CharField(
        verbose_name=u"Kategoria", choices=SPORT_CATEGORIES, max_length=16)

    class Meta:
        verbose_name = u"sport"
        verbose_name_plural = u"sporty"

    @classmethod
    def get_sports_choices(cls):
        choices = [('', '---------')]
        choices += [(s.pk, s.name) for s in cls.objects.all().order_by('name')]
        return choices


class Workout(CreatedAtMixin):
    name = models.CharField(
        verbose_name=u"Nazwa", max_length=64, null=True, blank=True)
    user = models.ForeignKey(
        User, verbose_name=u"Użytkownik", related_name='workouts')
    sport = models.ForeignKey('Sport', verbose_name=u"Dyscyplina")
    notes = models.CharField(
        verbose_name=u"Notatki", max_length=512, null=True, blank=True)
    distance = models.FloatField(
        verbose_name=u"Dystans", validators=[MinValueValidator(0)], null=True,
        blank=True)
    datetime_start = models.DateTimeField(verbose_name=u"Czas rozpoczęcia")
    datetime_stop = models.DateTimeField(verbose_name=u"Czas zakończenia")

    class Meta:
        verbose_name = u"trening"
        verbose_name_plural = u"treningi"

    def __unicode__(self):
        visible_name = self.sport.name
        if self.distance:
            visible_name += ", %s km" % str(self.distance)

        return visible_name

    def get_absolute_url(self):
        return reverse('workout_show', args=[self.pk])

    @property
    def duration(self):
        return self.datetime_stop - self.datetime_start

    @property
    def duration_visible(self):
        visible = str(self.datetime_stop - self.datetime_start)
        splitted = visible.split(':')
        return '%s godz. %s min. %s sek.' \
            % (splitted[0], splitted[1], splitted[2])

    def best_time_for_x_km(self, distance):
        """
        Get best time on x km

        :param distance: get time for this distance
        :return: fastest time for given distance
        :rtype: timedelta
        """

        if self.distance < distance:
            return

        # if there is no track
        try:
            return self.routes.get().best_time_for_x_km(distance)
        except ObjectDoesNotExist:
            proportions = distance / float(self.distance)
            return timedelta(seconds=int(proportions * self.duration.seconds))

    def best_time_for_x_mi(self, distance):
        """
        Get best time on x miles

        :param distance: get time for this distance
        :return: fastest time for given distance
        :rtype: timedelta
        """
        return self.best_time_for_x_km(mi2km(distance))
