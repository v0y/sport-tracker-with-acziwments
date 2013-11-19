# encoding: utf-8

import json
from xml.etree.cElementTree import parse

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required

from .forms import GPXForm


@login_required
@render_to('routes/routes.html')
def upload_gpx(request):
    """
    Tansform uploaded .gpx file to json and redirect
    to map page.
    """
    tracks = "{}"
    if request.method == 'POST':
        form = GPXForm(request.POST, request.FILES)
        if form.is_valid():
            # do some gpx to xml magic
            tracks = gpx_to_json(request.FILES['gpx_file'])
    else:
        form = GPXForm()

    return {'form': form, 'tracks': tracks}


def gpx_to_json(file_):
    tree = parse(file_)
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
                point = {
                    'lat': pt.attrib['lat'],
                    'lon': pt.attrib['lon'],
                    'ele': pt.find(ele_ns).text,
                    'time': pt.find(time_ns).text,
                }
                segment.append(point)
            track['segments'].append(segment)
        tracks.append(track)

    return json.dumps(tracks)
