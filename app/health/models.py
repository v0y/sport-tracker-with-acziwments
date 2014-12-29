# coding: utf-8

from datetime import (
    datetime,
    timedelta,
)

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)

from app.shared.helpers import get_date_format
from app.shared.models import RelatedDateMixin
from .enums import Range


class Health(RelatedDateMixin):
    user = models.ForeignKey(User, related_name='health')
    weight = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    fat = models.FloatField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    water = models.FloatField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )

    @classmethod
    def get_health_by_date(cls, user, range_type, date_str):
        """
        Get queryset of health datas by range

        :param user: user object
        :param range_type: dates range type - week, month or year
        :param date_str: date string
        :return: queryset of health datas
        :rtype: queryset
        """
        date_format = get_date_format(range_type)

        # get health queryset
        health = cls.objects.filter(user=user).order_by('related_date')

        if range_type in (Range.YEAR, Range.MONTH):
            date = datetime.strptime(date_str, date_format)
            health = health.filter(related_date__year=date.strftime('%Y'))
            if range_type == Range.MONTH:
                health = health.filter(related_date__month=date.strftime('%m'))

        elif range_type == Range.WEEK:
            date = datetime.strptime(date_str, date_format)
            start_date = date.strftime('%Y-%m-%d')
            end_date = date + timedelta(days=6)
            end_date = end_date.strftime('%Y-%m-%d')
            health = health.filter(related_date__range=[start_date, end_date])

        return health

    @classmethod
    def get_data(cls, user, range_type, date_str=None):
        """
        Get datas for health in pretty format

        :param user: user object
        :param range_type: dates range type - week, month, year or all-time
        :param date_str: date string
        :return: dict of health datas
        :rtype: dict of list of dicts

        **Return example**::

            [
                ['weight-y' 75, 74.5, 74.6],
                ['weight-x', '2013-01-01', '2013-01-02', '2013-01-03'],
                ['fat-y', 26.9, 26.7, 26],
                ['fat-x', '2013-01-01', '2013-01-02', '2013-01-03'],
                ['water-y', 50, 50.2, 50.2],
                ['water-x', '2013-01-01', '2013-01-02', '2013-01-03'],
            ]

        """

        # get datas by date
        health = Health.get_health_by_date(user, range_type, date_str)

        # create return dict
        data_dict = {
            'weight-y': ['weight-y'],
            'weight-x': ['weight-x'],
            'fat-y': ['fat-y'],
            'fat-x': ['fat-x'],
            'water-y': ['water-y'],
            'water-x': ['water-x'],
        }

        for h in health:
            date = h.related_date.strftime('%Y-%m-%d')
            if h.weight:
                data_dict['weight-y'].append(h.weight)
                data_dict['weight-x'].append(date)
            if h.fat:
                data_dict['fat-y'].append(h.fat)
                data_dict['fat-x'].append(date)
            if h.water:
                data_dict['water-y'].append(h.water)
                data_dict['water-x'].append(date)

        return_list = [v for v in data_dict.itervalues()]

        return return_list


    @classmethod
    def get_first_date(cls, user, date_format):
        """
        :param user: get date for this user object
        :param date_format: return date in this format
        :return: first date of registered health datas
        :rtype: datetime
        """

        health_qs = Health.objects.filter(user=user) \
            .order_by('related_date')

        def _get_first_date(type_, health_qs):
            """
            :param type_: type of health data: [weight | fat | water]
            :param health_qs: queryset of health objects
            :return: date of first given health type measurement
            """
            try:
                return {
                    'weight': health_qs.filter(weight__isnull=False),
                    'fat': health_qs.filter(fat__isnull=False),
                    'water': health_qs.filter(water__isnull=False),
                }[type_][0].related_date
            except (IndexError, KeyError):
                return None

        first_weight = _get_first_date('weight', health_qs)
        first_fat = _get_first_date('fat', health_qs)
        first_water = _get_first_date('water', health_qs)
        first_dates_list = filter(None, [first_weight, first_fat, first_water])

        if first_dates_list:
            first_date = min(first_dates_list)
            return first_date.strftime(date_format)
        else:
            return None
