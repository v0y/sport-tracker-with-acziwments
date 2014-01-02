# encoding: utf-8

import datetime
from urllib import unquote, urlencode
from urlparse import urlparse, urlunparse

from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify as django_slugify
from django.template.loader import render_to_string
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


def simple_send_email(
        subject, message, recipient_list,
        subject_data=None, message_data=None):
    """
    Send email using default email backend

    :param subject: String, email subject template (*.txt) or subject
    :param message: String, email content template (*.htm, *.html or *.txt)
                    or subject
    :param recipient_list: A list of strings, each an email address.
    :param subject_data: dict for extra data for subject template.
    :param message_data: dict for extra data for message template.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    fail_silently = False if settings.DEBUG else True
    allowed_message_template_extensions = ('.txt', '.html', '.htm')
    allowed_subject_template_extensions = ('.txt',)
    subject_data = subject_data or {}
    message_data = message_data or {}

    # parse message template
    if subject.endswith(allowed_subject_template_extensions):
        subject_str = render_to_string(subject, subject_data)
    else:
        subject_str = subject

    # parse subject template
    if message.endswith(allowed_message_template_extensions):
        message_str = render_to_string(message, message_data)
    else:
        message_str = message

    send_mail(subject_str, message_str, from_email, recipient_list,
              fail_silently=fail_silently)


def get_page(request, objects, per_page=10, few_visible=3):
    """
    Get paginator page

    :param objects: queryset of objects to paginate
    :param per_page: int, number of objects per page
    :param few_visible: numbers visible on beginning and ending of
                        paginator, like: [1, 2, 3 ... 7, 8, 9]
    :return: paginator page
    """
    paginator = Paginator(objects, per_page)
    num_pages = paginator.num_pages
    page = request.GET.get('page')

    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(num_pages)

    # set first and last visible pages ranges
    page.paginator.first_few = range(1, few_visible + 1)
    page.paginator.first_few_border = few_visible + 1
    page.paginator.last_few = range(num_pages - few_visible + 1, num_pages + 1)
    page.paginator.last_few_border = num_pages - few_visible

    return page


def slugify(s):
    """
    Slugify string

    :param s: string to slugify
    :return: slugified string
    """
    return django_slugify(unicode(s).replace(u'ł', 'l').replace(u'Ł', 'L'))


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
