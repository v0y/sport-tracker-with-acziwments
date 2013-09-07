# coding: utf-8

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver

from app.shared.models import CreatedAtMixin, SHA1TokenMixin
from .enums import SEX_SELECT


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, verbose_name=u'Użytkownik', related_name='profile')
    dob = models.DateField(verbose_name=u'Data urodzin', null=True, blank=True)
    sex = models.CharField(
        verbose_name=u'Płeć', max_length=1, choices=SEX_SELECT, null=True,
        blank=True)
    height = models.IntegerField(verbose_name=u'Wzrost', null=True, blank=True)

    class Meta:
        verbose_name = u'profil użytkownika'
        verbose_name_plural = u'profile użytkowników'

    @property
    def age(self):
        """
        :return: user age in years
        :rtype: int
        """
        delta = date.today() - self.dob
        return delta.days // 365

    @property
    def sex_visible(self):
        """
        :return: user sex for template
        :rtype: str
        """
        for k, v in SEX_SELECT:
            if k == self.sex:
                return v


class UserActivation(CreatedAtMixin, SHA1TokenMixin):
    user = models.OneToOneField(
        User, verbose_name=u'Użytkownik', related_name='activation')

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
        User, verbose_name=u'Użytkownik', related_name='password_reset')

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
        User, verbose_name=u'Użytkownik', related_name='email_activation')
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
def on_user_create(sender, instance, created, **kwargs):

    if created:
        # create user activation
        UserActivation.objects.create(user=instance)

        # create user extented profile
        UserProfile.objects.create(user=instance)
