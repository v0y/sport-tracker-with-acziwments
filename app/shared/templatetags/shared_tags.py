# coding: utf-8

from django import template
from django.core.urlresolvers import reverse

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
    tab_url = reverse(url_name, args=params)
    current_url = request.path_info
    if tab_url == current_url:
        return 'active'
    return ''
