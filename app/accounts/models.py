# coding: utf-8

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver

from app.shared.models import CreatedAtMixin, SHA1TokenMixin


class UserActivation(CreatedAtMixin, SHA1TokenMixin):
    user = models.OneToOneField(
        User, verbose_name='Użytkownik', related_name='activation')

    class Meta:
        verbose_name = u'aktywacja użytkownika'
        verbose_name_plural = u'aktywacje użytkowników'

    def get_activation_link(self):
        """
        Returns user activation link

        :returns: complete user activation link
        :rtype: str
        """
        url_name = 'registration_activation'
        return super(UserActivation, self).get_activation_link(url_name)


class PasswordReset(CreatedAtMixin, SHA1TokenMixin):
    user = models.OneToOneField(
        User, verbose_name='Użytkownik', related_name='password_reset')

    class Meta:
        verbose_name = u'reset hasła'
        verbose_name_plural = u'reset hasła'

    def get_password_reset_link(self):
        """
        Returns password reset link

        :returns: complete password reset link
        :rtype: str
        """
        url_name = 'password_reset_confirm'
        return super(PasswordReset, self).get_activation_link(url_name)


class EmailActivation(CreatedAtMixin, SHA1TokenMixin):
    user = models.OneToOneField(
        User, verbose_name='Użytkownik', related_name='email_activation')
    email = models.EmailField(verbose_name='Adres email')

    class Meta:
        verbose_name = u'aktywacja emaila'
        verbose_name_plural = u'aktywacja emaila'

    def get_activation_link(self):
        """
        Get new email activation link

        :returns: complete email change activation link
        :rtype: str
        """
        url_name = 'email_change_confirm'
        return super(EmailActivation, self).get_activation_link(url_name)


@receiver(post_save, sender=User)
def create_user_activation(sender, instance, created, **kwargs):
    if created:
        UserActivation.objects.create(user=instance)
