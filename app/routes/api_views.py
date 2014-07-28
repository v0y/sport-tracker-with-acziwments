# encoding: utf-8

from annoying.decorators import ajax_request
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Route


@ajax_request
@login_required
def upload_gpx(request):
    """
    Accept uploaded gpx file and create new route object.
    """
    # TODO: file validation
    gpx_file = request.FILES['gpx_file']
    if gpx_file:
        # save file to db
        route_id, tracks_json = Route.route_from_gpx(gpx_file, request)
        return {'id': route_id, 'tracks': tracks_json, 'info': 'OK'}

    return {'info': 'Error'}

@ajax_request
@login_required
def get_route_json(request):
    route_id = request.GET['route_id'][0]
    route = get_object_or_404(Route, pk=route_id)
    return {'route': route.tracks_json}


@ajax_request
@login_required
def save_route(request):
    route_data = request.POST['tracks']
    if route_data:
        route_id, tracks_json = Route.save_route(route_data, request)
        return {'id': route_id, 'tracks': tracks_json, 'info': 'OK'}

    return {'info': 'Error'}
