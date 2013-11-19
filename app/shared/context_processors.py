# coding: utf-8

from django.conf import settings


def settings_values(request):
    """
    Context processor, which sends setting values to templates.

    :return: dict of settings values
    """
    return {
        'DEBUG': settings.DEBUG,
        'GRAVATAR_CHANGE_URL': settings.GRAVATAR_CHANGE_URL,
        'GOOGLE_BROWSER_KEY': settings.GOOGLE_BROWSER_KEY,
    }
