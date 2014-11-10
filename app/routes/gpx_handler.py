# encoding: utf-8

from dateutil import parser as iso8601parser
from xml.etree.cElementTree import parse

from .helpers import get_distance, handle_datetime_string

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
