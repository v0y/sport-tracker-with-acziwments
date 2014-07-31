# encoding: utf-8

from datetime import datetime
import math
from pytz import UTC


def handle_datetime_string(datetime_str, datetime_format='%Y-%m-%d %H:%M:%S'):
    """
    :param datetime_str: time string
    :param datetime_format: format of time
    :return: datetime with UTC timezone
    :rtype: datetime
    """
    datetime_object = datetime.strptime(datetime_str, datetime_format)
    return datetime_object.replace(tzinfo=UTC)


def get_distance(point1, point2, round_to=False):
    """
    Get distance in kilometers between two points.

    :param point1: 1st point in format {'lat': 52., 'lon': 21.}
    :param point2: 2nd point in format {'lat': 52., 'lon': 21.}
    :return: distance in kilometers between given points
    :rtype: float
    """
    lat1, lon1 = point1['lat'], point1['lon']
    lat2, lon2 = point2['lat'], point2['lon']

    dlat = deg2rad(lat2 - lat1)
    dlon = deg2rad(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + (math.cos(deg2rad(lat1)) *
        math.cos(deg2rad(lat2)) * math.sin(dlon / 2) ** 2)
    distance = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) * 6371
    if round_to:
        distance = round(distance, round_to)

    return distance


def deg2rad(deg):
    return deg * (math.pi / 180)
