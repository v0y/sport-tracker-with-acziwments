# coding: utf-8

from django import template

register = template.Library()


@register.filter('klass')
def klass(ob):
    """Filter for getting object class

    * general usage: {{ object|klass }}
    * usage for widget type: {{ field.field.widget|klass }}

    :returns: object class
    """

    map_types = {
        'TextInput': 'text',
        'PasswordInput': 'password',
        'CheckboxInput': 'checkbox',
        # TODO: radio
        # TODO: textarea
    }

    return map_types[ob.__class__.__name__]
