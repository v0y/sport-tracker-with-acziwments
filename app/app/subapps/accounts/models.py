# coding: utf-8

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver

from app.subapps.shared.helpers import create_url
from app.subapps.shared.models import CreatedAtMixin, SHA1TokenMixin


class UserActivation(CreatedAtMixin, SHA1TokenMixin):
    user = models.OneToOneField(
        User, verbose_name='Użytkownik', related_name='activation'
    )

    class Meta:
        verbose_name = u'aktywacja użytkownika'
        verbose_name_plural = 'aktywacje użytkowników'

    def get_activation_link(self):
        """Returns user activation link"""
        # get site
        site = Site.objects.get(pk=settings.SITE_ID)

        # get activation link
        activation_url = create_url(scheme='http', url=site.domain,
                                    path=reverse('registration_activation'),
                                    params={'token': self.token})

        return activation_url


class PasswordReset(CreatedAtMixin, SHA1TokenMixin):
    user = models.OneToOneField(
        User, verbose_name='Użytkownik', related_name='password_reset'
    )

    class Meta:
        verbose_name = u'reset hasła'
        verbose_name_plural = 'reset hasła'

    def get_password_reset_link(self):
        """Returns user activation link"""
        # get site
        site = Site.objects.get(pk=settings.SITE_ID)

        # get password reset link
        reset_url = create_url(scheme='http', url=site.domain,
                               path=reverse('password_reset_confirm'),
                               params={'token': self.token})

        return reset_url


@receiver(post_save, sender=User)
def create_user_activation(sender, instance, created, **kwargs):
    if created:
        UserActivation.objects.create(user=instance)
