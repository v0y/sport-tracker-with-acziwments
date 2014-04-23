# encoding: utf-8

from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from timedelta.fields import TimedeltaField

from app.accounts.enums import UnitsTypes
from app.shared.helpers import mi2km, km2mi
from app.shared.models import CreatedAtMixin, NameMixin, SlugMixin
from .enums import SPORT_CATEGORIES, Unit, UNIT_CHOICES


class BestTime(models.Model):
    distance = models.ForeignKey('Distance')
    workout = models.ForeignKey('Workout')
    user = models.ForeignKey(User)
    unit = models.CharField(choices=UNIT_CHOICES, max_length=2)
    duration = TimedeltaField()

    class Meta:
        verbose_name = u"najlepszy czas"
        verbose_name_plural = u"najlepsze czasy"


class Distance(models.Model):
    unit = models.CharField(choices=UNIT_CHOICES, max_length=2)
    distance = models.FloatField()
    only_for = models.ManyToManyField(
        'Sport', null=True, blank=True,
        help_text=u"Jeśli podane, dystans pojawi się wyłącznie dla danych "
                  u"dyscyplin")
    name = models.CharField(verbose_name=u"Nazwa", max_length=64, blank=True)

    class Meta:
        verbose_name = u"dystans"
        verbose_name_plural = u"dystanse"
        unique_together = (('distance', 'unit'),)
        ordering = ['id']

    def __unicode__(self):
        return self.name or "%s %s" % (self.distance, self.unit)

    @property
    def distance_km(self):
        return self.distance if self.unit == 'km' else mi2km(self.distance)


class Sport(NameMixin, SlugMixin):
    category = models.CharField(
        verbose_name=u"Kategoria", choices=SPORT_CATEGORIES, max_length=16)
    show_distances = models.BooleanField(default=True)
    show_map = models.BooleanField(default=True)

    class Meta:
        verbose_name = u"sport"
        verbose_name_plural = u"sporty"

    @classmethod
    def get_sports_choices(cls):
        choices = [('', '---------')]
        choices += [(s.pk, s.name) for s in cls.objects.all().order_by('name')]
        return choices

    def get_distances(self, unit=None):
        assert unit in (None, Unit.kilometers, Unit.miles)
        if not self.show_distances:
            return
        unit = unit or UnitsTypes.metric
        distances = Distance.objects.filter(only_for=None, unit=unit)
        return distances | self.distance_set.filter(unit=unit)


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
    is_active = models.BooleanField(
        verbose_name=u"Włączony do statystyk", default=True)

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

    def update_best_time(self, distance):
        """
        Update or create best time object for given distance

        :param distance: distance object
        :return: None
        """
        best_times = BestTime.objects.filter(distance=distance, workout=self)

        if best_times.exists():
            duration = self.best_time_for_x_km(distance.distance)
            best_times.update(duration=duration)
        else:
            BestTime.objects.create(
                distance=distance, unit=distance.unit, workout=self,
                duration=self.best_time_for_x_km(distance.distance),
                user=self.user)


@receiver(post_save, sender=Workout)
def update_best_times(sender, instance, **kwargs):
    if instance.distance:
        distances = Distance.objects.filter(
            Q(distance__lte=instance.distance, unit='km') |
            Q(distance__lte=km2mi(instance.distance), unit='mi'))

        for distance in distances:
            instance.update_best_time(distance)
