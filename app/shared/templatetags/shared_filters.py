# coding: utf-8

from django import template

register = template.Library()


@register.filter('field_type')
def field_type(widget):
    """Filter for getting field type

    usage: {{ field.field.widget|field_type }}

    :returns: field type
    """

    map_types = {
        'TextInput': 'text',
        'PasswordInput': 'password',
        'CheckboxInput': 'checkbox',
        'DateInput': 'date',
        # TODO: radio
        # TODO: textarea
    }

    return map_types[widget.__class__.__name__]
