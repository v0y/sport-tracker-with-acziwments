# encoding: utf-8

from collections import defaultdict
from datetime import (
    datetime,
)

from app.shared.enums import ChartTimeRange
from app.shared.helpers import get_date_format
from .models import (
    Sport,
    Workout,
)


class DistanceChart(object):
    def __init__(self, user, range_type, date=None):
        self.date_format = get_date_format(range_type)
        self.range_type = range_type
        self.user = user
        if date:
            self.date = datetime.strptime(date, self.date_format)
        self.queryset = self._get_queryset()

    def _get_queryset(self):
        # get health queryset
        workouts = Workout.objects \
            .filter(user=self.user) \
            .order_by('datetime_start')

        if self.range_type in (ChartTimeRange.YEAR, ChartTimeRange.MONTH):
            workouts = workouts.filter(datetime_start__year=self.date.year)

        if self.range_type == ChartTimeRange.MONTH:
            workouts = workouts.filter(datetime_start__month=self.date.month)

        return workouts

    def _get_disciplines(self):
        disciplines = self.queryset.values_list('sport', flat=True)
        return Sport.objects.filter(id__in=disciplines)

    def _get_alltime_data(self, discipline, year_start, year_end):
        years_range = range(year_start, year_end + 1)
        dates = ['%s-' % year for year in years_range]
        data = {}
        for date in years_range:
            data[date] = float()
        workouts = self.queryset.filter(sport=discipline)

        for workout in workouts:
            if workout.distance:
                data[workout.datetime_start.year] += workout.distance

        # return None if there is no distance
        total_distance = float()
        values = list(data.itervalues())
        for distance in values:
            total_distance += distance

        if not total_distance:
            return None
        else:
            return dates, list(values)

    def _get_year_data(self, discipline):
        """
        :param discipline: discipline object
        :return: x data (months), y data (kilometers)
        :rtype: tuple
        """
        dates = ['%s-%s' % (self.date.year, month) for month in xrange(1, 13)]
        data = {}
        for date in xrange(1, 13):
            data[date] = float()
        workouts = self.queryset.filter(sport=discipline)

        for workout in workouts:
            if workout.distance:
                data[workout.datetime_start.month] += workout.distance

        return dates, list(data.itervalues())

    def _get_data(self, *args, **kwargs):
        return {
            ChartTimeRange.ALLTIME: self._get_alltime_data,
            ChartTimeRange.YEAR: self._get_year_data,
            # ChartTimeRange.MONTH: self._get_month_data,
            # ChartTimeRange.WEEK: self._get_week_data,
        }[self.range_type](*args, **kwargs)

    def get_data(self):
        disciplines = self._get_disciplines()
        data_dict = defaultdict(list)
        data_list = []

        # get min and max year
        if self.range_type == ChartTimeRange.ALLTIME:
            year_start = self.queryset.first().datetime_start.year
            year_end = self.queryset.last().datetime_start.year
            # get workouts for disciplines
            for discipline in disciplines:
                data = self._get_data(discipline, year_start, year_end)
                if data:
                    data_dict[discipline.name] = data
        else:
            # get workouts for disciplines
            for discipline in disciplines:
                data = self._get_data(discipline)
                if data:
                    data_dict[discipline.name] = data

        # adapt to c3 charts data format
        for discipline_name, data in data_dict.iteritems():
            x_data = data[0]
            x_data.insert(0, '%s-x' % discipline_name)

            y_data = data[1]
            y_data.insert(0, discipline_name)

            data_list.append(x_data)
            data_list.append(y_data)

        return data_list
