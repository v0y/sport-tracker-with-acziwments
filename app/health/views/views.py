# encoding: utf-8

from datetime import datetime

from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import (
    Http404,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from fiut.helpers import get_page_and_paginator

from ..forms import HealthForm
from ..helpers import get_and_validate_date
from ..models import Health


@login_required
@render_to('health/health_form.html')
def add_health(request):
    """
    Add health entry
    """
    form = HealthForm(
        request.POST or None,
        initial={'related_date': datetime.now().strftime('%d-%m-%Y')})
    if form.is_valid():
        pre_saved_form = form.save(commit=False)
        pre_saved_form.user = request.user
        pre_saved_form.save()
        return redirect(reverse('health:show_charts'))
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
        form.user = request.user
        form.save()
        return redirect('health:show_list')
    return {'form': form}


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
    url_is_complete = bool(date) or range_type == 'all-time'

    date = get_and_validate_date(range_type, date)

    # get user
    user = get_object_or_404(User, username=username)
    # TODO: check, if user wants to share his stats

    # redirect with date
    if not url_is_complete:
        args = [username, range_type]
        if date:
            args.append(date)

        return redirect(reverse('health:show_charts', args=args))

    # get first date of registered health datas
    first_date = Health.get_first_date(user, '%Y-%m-%d')

    return {'first_date': first_date}


@login_required
@render_to('health/show_list.html')
def health_show_list(request, username=None):
    """
    Show health list with edit link
    """
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    health = Health.objects.filter(user=user).order_by('-related_date')
    page, _ = get_page_and_paginator(request, health, 25)

    return {
        'page': page,
        'is_mine': user == request.user
    }
