# coding: utf-8

from django import template
from django.template import Context
from django.template.loader import get_template

register = template.Library()


@register.filter
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
        'DateInput': 'text',
        'TimeInput': 'text',
        'EmailInput': 'email',
        'NumberInput': 'text',
        'Select': 'selection',
        'DateTimeInput': 'text',
        'Textarea': 'textarea',
        'SelectDateWidgetWithNone': 'special',
        # TODO: radio
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
def bootstrap(field, addon=''):
    if addon:
        splitted_addon = addon.split('|')
        addon_type = splitted_addon[0]
        try:
            addon_text = splitted_addon[1]
        except IndexError:
            addon_text = ''
    else:
        addon_type = ''
        addon_text = ''

    context = Context(
        {'field': field, 'addon': addon_type, 'addon_text': addon_text})
    return get_template("snippets/field.html").render(context)
