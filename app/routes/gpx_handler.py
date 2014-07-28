# encoding: utf-8

from datetime import datetime, timedelta, tzinfo
import math
from pytz import UTC
from xml.etree.cElementTree import parse

from dateutil import parser as iso8601parser


def handle_gpx(gpx_file, round_distance_to=False):
    # convert gpx to tracks
    tracks = gpx_to_tracks(gpx_file)

    # get additional route data
    start_time, finish_time = get_start_and_finish_times(tracks)
    length, height_up, height_down = \
        get_distance_and_elevations_delta(tracks, round_distance_to)

    return tracks, start_time, finish_time, length, height_up, height_down


def gpx_to_tracks(gpx_file):
    tree = parse(gpx_file)
    root = tree.getroot()
    namespace = root.tag[:-3]

    # prepare tag identyfiers with namespace
    type_id = '%stype' % namespace
    ele_ns = '%sele' % namespace
    time_ns = '%stime' % namespace

    # get tracks
    tracks = []
    for trk in root.getiterator('%strk' % namespace):
        track = {}

        # track type (eg. RUNNING)
        type_ = trk.find(type_id)
        if type_:
            track['type'] = type_.text

        track['segments'] = []

        for seg in trk.findall('%strkseg' % namespace):
            segment = []
            for pt in seg:
                # convert iso 8601 to string suitable for javascript conversion
                time = iso8601parser.parse(pt.find(time_ns).text) \
                    .strftime("%Y-%m-%d %H:%M:%S")
                point = {
                    'lat': float(pt.attrib['lat']),
                    'lon': float(pt.attrib['lon']),
                    'ele': float(pt.find(ele_ns).text),
                    'time': time,
                }
                segment.append(point)
            track['segments'].append(segment)
        tracks.append(track)

    return tracks


def get_segment_dist_and_ele(segment, round_distance_to=False):
    distance = 0
    delta_elevation_up = 0
    delta_elevation_down = 0
    i = 1
    while i < len(segment):
        point1 = segment[i - 1]
        point2 = segment[i]

        # get distance
        distance += get_distance(point1, point2)

        # get height difference
        d_ele = point2.get('ele', 0) - point1.get('ele', 0)
        if d_ele > 0:
            delta_elevation_up += d_ele
        else:
            delta_elevation_down += d_ele

        # update counter
        i += 1

    if round_distance_to:
        distance = round(distance, round_distance_to)

    return distance, delta_elevation_up, delta_elevation_down


def get_distance_and_elevations_delta(tracks, round_distance_to=False):
    distance = 0
    delta_elevation_up = 0
    delta_elevation_down = 0
    for track in tracks:
        for segment in track['segments']:
            distance, delta_elevation_up, delta_elevation_down = \
                get_segment_dist_and_ele(segment)

    if round_distance_to:
        distance = round(distance, round_distance_to)

    return distance, delta_elevation_up, delta_elevation_down


def get_segment_start_and_finish_times(segment):
    start = segment[0]['time']
    finish = segment[-1]['time']
    return handle_datetime_string(start), handle_datetime_string(finish)


def get_start_and_finish_times(tracks):
    start = tracks[0]['segments'][0][0]['time']
    finish = tracks[-1]['segments'][-1][-1]['time']
    return handle_datetime_string(start), handle_datetime_string(finish)


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
