# encoding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import RedirectView, TemplateView

from .views import SettingsView, ShowUserProfileView


urlpatterns = patterns('app.accounts.views',
    # login
    url(r'^/login$', 'login_view', name='login'),
    url(r'^/logout$', 'logout_view', name='logout'),
    # registration
    url(r'^/registration$', 'registration', name='registration'),
    url(r'^/registration/end$', 'registration_end',
        name='registration_end'),
    url(r'^/registration/activation$', 'registration_activation',
        name='registration_activation'),
    # activation
    url(r'^/registration/activation/failed$',
        TemplateView.as_view(
            template_name='accounts/registration_activation_failed.html'),
        name='registration_activation_failed'),
    url(r'^/registration/activation/end$',
        TemplateView.as_view(
            template_name='accounts/registration_activation_end.html'),
        name='registration_activation_end'),
    url(r'^/registration/activation/resend$', 'registration_activation_resend',
        name='registration_activation_resend'),
    url(r'^/registration/activation/resend/end$',
        TemplateView.as_view(
            template_name='accounts/registration_activation_resend_end.html'),
        name='registration_activation_resend_end'),
    # change password
    url(r'^/password/change$', 'password_change', name='password_change'),
    url(r'^/password/change/end$',
        TemplateView.as_view(
            template_name='accounts/password_change_end.html'),
        name='password_change_end'),
    # reset password
    url(r'^/password/reset$', 'password_reset', name='password_reset'),
    url(r'^/password/reset/end$',
        TemplateView.as_view(
            template_name='accounts/password_reset_end.html'),
        name='password_reset_end'),
    url(r'^/password/reset/confirm$', 'password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^/password/reset/confirm/end$',
        TemplateView.as_view(
            template_name='accounts/password_reset_confirm_end.html'),
        name='password_reset_confirm_end'),
    url(r'^/password/reset/confirm/failed$',
        TemplateView.as_view(
            template_name='accounts/password_reset_failed.html'),
        name='password_reset_failed'),
    # ajax
    url(r'^/api/check_username$', 'is_username_used',
        name='is_username_used'),
    url(r'^/api/check_email$', 'is_email_used', name='is_email_used'),
    # user profile
    url(r'^/show/(?P<username>[\w.@+-]+)$',
        ShowUserProfileView.as_view(), name='profile'),
    url(r'^/settings$', RedirectView.as_view(pattern_name='profile_settings')),
    url(r'^/settings/profile$', 'profile_settings', name='profile_settings'),
    url(r'^/settings/website$',
        SettingsView.as_view(), name='website_settings'),
    # change email
    url(r'^/settings/email/change$', 'email_change', name='email_change'),
    url(r'^/settings/email/change/end$', 'email_change_end',
        name='email_change_end'),
    url(r'^/settings/email/change/confirm$', 'email_change_confirm',
        name='email_change_confirm'),
    url(r'^/settings/email/change/confirm/failed$',
        TemplateView.as_view(
            template_name='accounts/email_change_confirm_failed.html'),
        name='email_change_confirm_failed'),
    url(r'^/settings/email/change/confirm/end$', 'email_change_confirm_end',
        name='email_change_confirm_end'),
)
