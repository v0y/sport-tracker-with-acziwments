# coding: utf-8

from django import template
from django.template import Context
from django.template.loader import get_template

register = template.Library()


@register.filter('field_type')
def field_type(widget):
    """
    Filter for getting field type

    **Usage**::

        {{ field.field.widget|field_type }}

    :returns: field type
    """

    map_types = {
        'TextInput': 'text',
        'PasswordInput': 'password',
        'CheckboxInput': 'checkbox',
        'DateInput': 'date',
        'EmailInput': 'email',
        # TODO: radio
        # TODO: textarea
    }

    return map_types[widget.__class__.__name__]


@register.filter('I_dont_want_None')
def I_dont_want_None(val):
    """
    If value is None, returns empty string

    :param val: value to check if is not None
    :returns: value if not None, otherwise empty string
    """

    return val if val is not None else ''


@register.filter
def bootstrap(field, addon=False):
    context = Context({'field': field, 'addon': addon})
    return get_template("snippets/field.html").render(context)
