# coding: utf-8

from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def is_active_tab(request, url_name, *parameters):
    """
    Check, if given tab is active

    :param request: guess what?
    :param url_name: tab url name (from urls.py)
    :param parameter: parameter for url
    :return: string "active" if tab is active
    """
    tab_url = reverse(url_name, args=list(parameters))
    current_url = request.path_info
    if tab_url == current_url:
        return 'active'
