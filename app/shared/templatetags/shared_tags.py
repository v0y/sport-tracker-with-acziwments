# coding: utf-8

from django import template
from django.core.urlresolvers import NoReverseMatch, reverse

register = template.Library()


@register.simple_tag
def is_active_tab(request, url_name, *params):
    """
    Check, if given tab is active

    **Usage**::

        {% is_active_tab request 'url_name' %}
        {% is_active_tab request 'url_name' request.parameter %}

    :param request: guess what?
    :param url_name: tab url name (from urls.py)
    :param parameter: parameter for url
    :return: string "active" if tab is active, else empty string
    :rtype: str
    """
    try:
        tab_url = reverse(url_name, args=params)
    except NoReverseMatch:
        return ''

    if tab_url == request.path_info:
        return 'active'
    return ''
