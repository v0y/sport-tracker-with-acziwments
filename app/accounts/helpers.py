# coding: utf-8

import json
from os.path import dirname, join, realpath

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def get_mail_provider_url(email):
    """
    Get url to provider of given email address

    :param email: email address
    :return: url to email's provider login page
    """
    try:
        validate_email(email)
    except ValidationError:
        return None

    original_email_alias = email.split('@')[1]
    path = join(dirname(realpath(__file__)), 'emails_providers.json')
    emails_providers_json = open(path)
    emails_providers = json.load(emails_providers_json)
    for email_provider, email_aliases in emails_providers.iteritems():
        if original_email_alias in email_aliases:
            return 'http://' + email_provider
