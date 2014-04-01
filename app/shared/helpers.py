# encoding: utf-8

import datetime
from urllib import unquote, urlencode
from urlparse import urlparse, urlunparse

from django.utils import timezone


def create_url(scheme='', url='', path='', params=None):
    """
    Creates URI by adding GET parameters to URL

    :param scheme: url scheme, e.g. 'http'
    :param url: base url, e.g. 'example.com'
    :param path: patch, e.g. '/foo/bar/baz'
    :param params: dict of GET parameters, e.g. {'key': 'val'}
    """
    if not (scheme or url or path):
        return
    params = params or {}

    url = scheme + '://' + url if scheme else url
    url += path
    url_parts = list(urlparse(url))
    url_parts[4] = unquote(urlencode(params))
    url = urlunparse(url_parts)
    return url


def get_date_format(date_type):
    """
    :param date_type: "week", "month" or "year"
    :return: date format
    """
    return {
        'week': '%Y-%m-%d',
        'month': '%Y-%m',
        'year': '%Y'}[date_type]


def unix_time(datetime_):
    """
    :param datetime_: datetime object with or without timezone
    :return: unix time for given datetime
    """
    epoch = datetime.datetime.utcfromtimestamp(0)

    if timezone.is_aware(datetime_):
        epoch = timezone.make_aware(epoch, timezone.utc)

    delta = datetime_ - epoch

    return delta.total_seconds()


def km2mi(km):
    """
    Converts miles to kilometers

    :param km: kilometers to convert to miles
    :return: kilometers converted to miles
    :rtype: float
    """
    return km * 0.621371


def mi2km(mi):
    """
    Converts miles to kilometers

    :param mi: miles to convert to kiloeters
    :return: miles converted to kilometers
    :rtype: float
    """
    return mi * 1.60934
