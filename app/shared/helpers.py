# encoding: utf-8

from urllib import unquote, urlencode
from urlparse import urlparse, urlunparse

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def create_url(scheme='', url='', path='', params={}):
    """
    Creates URI by adding GET parameters to URL

    :param scheme: url scheme, e.g. 'http'
    :param url: base url, e.g. 'example.com'
    :param path: patch, e.g. '/foo/bar/baz'
    :param params: dict of GET parameters, e.g. {'key': 'val'}
    """
    if not (scheme or url or path):
        return
    url = scheme + '://' + url if scheme else url
    url += path
    url_parts = list(urlparse(url))
    url_parts[4] = unquote(urlencode(params))
    url = urlunparse(url_parts)
    return url


def simple_send_email(subject, message, recipient_list,
                      subject_data={}, message_data={}):
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
    allowed_subject_template_extensions = ('.txt')

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
