# coding: utf-8

from datetime import date, datetime, timedelta
from pytz import UTC

from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver

from app.health.models import Health
from app.shared.models import CreatedAtMixin, SHA1TokenMixin
from app.workouts.models import Sport
from .enums import SEX_SELECT


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, verbose_name=u'Użytkownik', related_name='profile')
    dob = models.DateField(verbose_name=u'Data urodzin', null=True, blank=True)
    sex = models.CharField(
        verbose_name=u'Płeć', max_length=1, choices=SEX_SELECT, null=True,
        blank=True)
    height = models.IntegerField(verbose_name=u'Wzrost', null=True, blank=True)

    class Meta:
        verbose_name = u'profil użytkownika'
        verbose_name_plural = u'profile użytkowników'

    @property
    def age(self):
        """
        :return: user age in years
        :rtype: int
        """
        delta = date.today() - self.dob
        return delta.days // 365

    @property
    def sex_visible(self):
        """
        :return: user sex for template
        :rtype: str
        """
        for k, v in SEX_SELECT:
            if k == self.sex:
                return v

    @property
    def last_weight(self):
        """
        Get last user weight

        :return: tuple of last weight and date of last weighting or None
        :rtype: tuple
        """
        user = self.user
        health_list = Health.objects.filter(user=user, weight__isnull=False). \
            order_by('-related_date')
        if health_list:
            return health_list[0].weight, health_list[0].related_date
        else:
            return None

    @property
    def bmi(self):
        """
        Compute BMI for last weighting

        :return: tuple of user BMI and date of last weighting
        :rtype: tuple
        """

        # validate height
        try:
            height_in_meters = float(self.height) / 100
        except TypeError:
            return None

        # get weight and date
        try:
            weight, date_ = self.last_weight
        except TypeError:
            return None

        # compute BMI
        bmi = weight / height_in_meters ** 2

        return round(bmi, 1), date_

    @property
    def favourite_sport(self):
        """
        1. get discipline with most workouts in last year
        2. If there is no workouts in last year - get from all workouts

        :return: favourite discipline object
        """
        year_ago = datetime.now(tz=UTC) - timedelta(days=365)

        sport_base_qs = Sport.objects \
            .filter(workout__user=self.user, workout__is_active=True) \
            .annotate(workouts_count=Count('workout'))

        favourite_sport = sport_base_qs \
            .filter(workout__datetime_stop__gt=year_ago) \
            .order_by('-workouts_count', '-workout__datetime_stop') \
            .first()

        if favourite_sport:
            return favourite_sport
        else:
            return sport_base_qs \
                .order_by('-workouts_count', '-workout__datetime_stop') \
                .first()

    def get_sports_in_year(self, year=None):
        """
        Returns list of sports from workouts in given calendar year
        sorted by workouts number.

        If year is not given use current year.

        :param year: int, year
        :return: sports from given year workouts
        :rtype: list
        """
        year = year or date.today().year

        sports = Sport.objects \
            .filter(
                workout__user=self.user,
                workout__is_active=True,
                workout__datetime_stop__year=year) \
            .annotate(workouts_count=Count('workout')) \
            .filter(workouts_count__gt=0) \
            .order_by('-workouts_count', '-workout__datetime_stop')
        return list(sports)


class UserActivation(CreatedAtMixin, SHA1TokenMixin):
    user = models.OneToOneField(
        User, verbose_name=u'Użytkownik', related_name='activation')

    class Meta:
        verbose_name = u'aktywacja użytkownika'
        verbose_name_plural = u'aktywacje użytkowników'

    @property
    def activation_link(self):
        """
        Returns user activation link

        :returns: complete user activation link
        :rtype: str
        """
        return self.get_activation_link('registration_activation')


class PasswordReset(CreatedAtMixin, SHA1TokenMixin):
    user = models.OneToOneField(
        User, verbose_name=u'Użytkownik', related_name='password_reset')

    class Meta:
        verbose_name = u'reset hasła'
        verbose_name_plural = u'reset hasła'

    def get_password_reset_link(self):
        """
        Returns password reset link

        :returns: complete password reset link
        :rtype: str
        """
        url_name = 'password_reset_confirm'
        return super(PasswordReset, self).get_activation_link(url_name)


class EmailActivation(CreatedAtMixin, SHA1TokenMixin):
    user = models.OneToOneField(
        User, verbose_name=u'Użytkownik', related_name='email_activation')
    email = models.EmailField(verbose_name='Adres email')

    class Meta:
        verbose_name = u'aktywacja emaila'
        verbose_name_plural = u'aktywacja emaila'

    @property
    def activation_link(self):
        """
        Get new email activation link

        :returns: complete email change activation link
        :rtype: str
        """
        return self.get_activation_link('email_change_confirm')


@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, **kwargs):

    if created:
        # create user activation
        UserActivation.objects.create(user=instance)

        # create user extented profile
        UserProfile.objects.create(user=instance)
