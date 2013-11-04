# encoding: utf-8

from datetime import datetime
import json
from re import match

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from app.shared.helpers import get_page
from .forms import HealthForm
from .models import Health


@login_required
@render_to('health/health_form.html')
def add_health(request):
    """
    Add health entry
    """
    form = HealthForm(request.POST or None)
    if form.is_valid():
        pre_saved_form = form.save(commit=False)
        pre_saved_form.user = request.user
        pre_saved_form.save()
        return redirect(reverse('health_show_charts'))
    return {'form': form}


@login_required
@render_to('health/health_form.html')
def edit_health(request, pk):
    """
    Edit health entry
    """
    # get health
    health = get_object_or_404(Health, pk=pk)
    # check permission to edit
    if health.user != request.user:
        raise Http404

    form = HealthForm(request.POST or None, instance=health)
    if form.is_valid():
        pre_saved_form = form.save(commit=False)
        pre_saved_form.user = request.user
        pre_saved_form.save()
        return redirect(reverse('health_show_list'))
    return {'form': form}


def _get_and_validate_date(range_type, date=None):
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
        date = '%s-%s' % (today.year, today.month)

    # check, if regex is valid for chosen range type
    if not match(regex, date):
        raise Http404

    return date


@login_required
@render_to('health/show_charts.html')
def health_show_charts(request, username=None, range_type='month', date=None):
    """
    Show health charts

    :param username: show charts for this username
    :param range_type: chart type - for week, month or year.
                       Default: month
    :param date: show chart from this date. Default: this month.
                 Valid formats:
                 
                 * ``yyyy-mm-dd`` for week - this is week start date
                 * ``yyyy-mm`` for month - show chart for this month
                 * ``yyyy`` for year - chow chart for this year

    """
    # get username
    username = username or request.user.username

    # url without date?
    url_is_complete = bool(date)

    date = _get_and_validate_date(range_type, date)

    # get user
    user = get_object_or_404(User, username=username)
    # TODO: check, if user wants to share his stats

    # redirect with date
    if not url_is_complete:
        return redirect(
            reverse('health_show_charts', args=[username, range_type, date]))

    # get first date of registered health datas
    first_date = Health.get_first_date(user, '%Y-%m-%d')

    return {'first_date': first_date}


@csrf_exempt
def health_api(request):
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
    _get_and_validate_date(range_type, date)

    # get dict data
    data_dict = Health.get_datas(user, range_type, date)

    # return json
    return HttpResponse(json.dumps(data_dict), content_type="application/json")


@login_required
@render_to('health/show_list.html')
def health_show_list(request, username=None):
    """
    Show health list with edit link
    """
    user = get_object_or_404(User, username=username) if username \
        else request.user
    health = Health.objects.filter(user=user).order_by('-related_date')
    page = get_page(request, health, 50)

    return {
        'page': page,
        'is_mine': user == request.user}
