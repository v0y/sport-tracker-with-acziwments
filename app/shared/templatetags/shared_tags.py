# coding: utf-8

from django import template
from django.core.urlresolvers import (
    NoReverseMatch,
    reverse,
)

register = template.Library()


@register.simple_tag
def is_active_tab(request, url, *params):
    """
    Check, if given tab is active

    **Usage**::

        {% is_active_tab 'url_startswith' %}

    :param url: first part of url path with starting '/'
    :param params: parameters for url
    :return: string "active" if tab is active, else empty string
    :rtype: str
    """

    if request.path_info.startswith(url):
        return 'active'

    try:
        tab_url = reverse(url, args=params)
    except NoReverseMatch:
        return ''

    if tab_url == request.path_info:
        return 'active'

    return ''
