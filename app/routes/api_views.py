# encoding: utf-8

from annoying.decorators import ajax_request
from django.contrib.auth.decorators import login_required

from .models import Route

@ajax_request
@login_required
def upload_gpx(request):
    """
    Accept uploaded gpx file and create new route object.
    """
    # TODO: file validation
    if request.FILES['gpx_file']:
        # save file to db
        id, tracks_json = Route.route_from_gpx(request.FILES['gpx_file'], request)
        return {'id': id, 'tracks': tracks_json, 'info': 'OK'}

    return {'info': 'Error'}