# encoding: utf-8

from datetime import datetime
from re import match

from django.http import Http404


def get_and_validate_date(range_type, date=None):
    """
    Return date if valid, else raise 404

    :param range_type: week, month or year
    :param date: date to validate. Valid formats:
                 * ``yyyy-mm-dd`` for week - this is week start date
                 * ``yyyy-mm`` for month - show chart for this month
                 * ``yyyy`` for year - chow chart for this year
    :return: date. If date was None, todays date for range_type==month
    :rtype: str
    :raise: Http404
    """
    # get regex
    regex = {
        'week': r'^[\d]{4}-[\d]{2}-[\d]{2}$',
        'month': r'^[\d]{4}-[\d]{2}$',
        'year': r'^[\d]{4}$'}[range_type]

    # get date if not given
    if not date:
        today = datetime.now()
        date = '%s-%s' % (today.year, str(today.month).zfill(2))

    # check, if regex is valid for chosen range type
    if not match(regex, date):
        raise Http404

    return date
