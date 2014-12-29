# encoding: utf-8

import json

from django.contrib.auth.models import User
from django.http import (
    Http404,
    HttpResponse,
)
from django.shortcuts import (
    get_object_or_404,
)
from ..helpers import get_and_validate_date
from ..models import Health


def health_chart_api(request):
    """
    Return health data as json

    Required POST values:

    * username: get data for this username
    * range_type: get data for week, month or year.
    * date: show chart from this date. Valid formats:

      * ``yyyy-mm-dd`` for week - this is week start date
      * ``yyyy-mm`` for month - show chart for this month
      * ``yyyy`` for year - chow chart for this year

    :return: health datas for given user and period
    :rtype: json
    """

    # get values from POST
    try:
        username = request.POST['username']
        range_type = request.POST['range_type']
        date = request.POST['date']
    except (KeyError, TypeError):
        raise Http404

    # get user or raise 404
    user = get_object_or_404(User, username=username)

    # validate date, if invalid raise 404
    get_and_validate_date(range_type, date)

    # get dict data
    data_dict = Health.get_data(user, range_type, date)

    # return json
    return HttpResponse(json.dumps(data_dict), content_type="application/json")
