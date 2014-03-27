# coding: utf-8

from datetime import datetime

from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView

from app.activities.models import Activity
from app.activities.views import render_activities
from .forms import (ChangeEmailForm, ChangePasswordForm, LoginForm,
    NewPasswordForm, PasswordResetForm, RegistrationForm,
    ResendActivationMailForm, UserProfileForm)
from .helpers import get_mail_provider_url
from .models import EmailActivation, UserActivation, PasswordReset
from app.shared.helpers import create_url, simple_send_email


class ShowUserProfileView(DetailView):
    model = User
    template_name = 'accounts/user_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(ShowUserProfileView, self).get_context_data(**kwargs)

        # get activities
        activities = Activity.objects.filter(user=self.object) \
            .order_by('-related_date', '-created_at')

        # render activities
        context['activities'] = render_activities(activities)
        return context


@render_to('accounts/login.html')
def login_view(request):
    """
    login user
    """

    # if logged in, redirect to login success page
    if request.user.is_authenticated():
        return redirect(getattr(settings, 'REDIRECT_AFTER_LOGIN', '/'))

    # get login form
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check authentication data
        user = authenticate(username=username, password=password)
        if user is None:
            return {
                'form': form,
                'error': u"Nieprawidłowy login lub hasło"
            }

        # check, if account is activated
        elif not user.is_active:
            return {
                'form': form,
                'error': u"Twoje konto nie zostało aktywowane"
            }

        login(request, user)

        return redirect(
            request.GET.get('next') or
            getattr(settings, 'REDIRECT_AFTER_LOGIN', '/'))

    return {'form': form}


def logout_view(request):
    """
    Log out user
    """
    logout(request)
    return redirect(getattr(settings, 'REDIRECT_AFTER_LOGOUT', '/'))


@render_to('accounts/registration.html')
def registration(request):
    """
    Create new account
    """

    # if logged in, redirect to login success page
    if request.user.is_authenticated():
        return redirect(settings.REDIRECT_AFTER_LOGIN)

    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # create user
        u = User(username=username, email=email, is_active=False)
        u.set_password(password)
        u.save()

        # get activation link
        activation_url = u.activation.activation_link

        # get site
        site = get_current_site(request)

        message_data = {
            'site_name': site.name,
            'activation_url': activation_url,
            'username': username
        }

        # send email
        simple_send_email(
            'accounts/emails/registration_subject.txt',
            'accounts/emails/registration_content.txt',
            [email],
            subject_data={'site_name': site.name},
            message_data=message_data)

        request.session['email'] = email
        # redirect to end registration page
        redirect_url = reverse('registration_end')
        return redirect(redirect_url)

    return {'form': form}


@render_to("accounts/registration_end.html")
def registration_end(request):
    """
    Show after registration page
    """
    email = request.session.get('email')
    email_provider = get_mail_provider_url(email)
    return {
        'email_provider': email_provider,
        'email': request.session.get('email')
    }


def registration_activation(request):
    """
    Activate account and delete used token
    """
    token = request.GET.get('token', '')

    # check token
    activation = get_object_or_None(UserActivation, token=token)
    if not activation:
        return redirect('registration_activation_failed')

    # activate user
    user = activation.user
    user.is_active = True
    user.save()

    # delete used token
    activation.delete()

    return redirect('registration_activation_end')


@render_to('accounts/registration_activation_resend.html')
def registration_activation_resend(request):
    """
    Resend activation email
    """

    form = ResendActivationMailForm(request.POST or None)

    if form.is_valid():
        username_or_email = request.POST['username_or_email']

        # get user
        if username_or_email.find('@') >= 0:
            user = get_object_or_None(User, email=username_or_email)
        else:
            user = get_object_or_None(User, username=username_or_email)

        # delete old activation
        activation = user.activation
        activation.delete()

        # generate new activation link
        activation = UserActivation.objects.create(user=user)

        # get activation link
        activation_url = activation.activation_link

        site = get_current_site(request)
        # send email
        message_data = {
            'site_name': site.name,
            'activation_url': activation_url,
            'username': user.username
        }

        simple_send_email(
            'accounts/emails/registration_subject.txt',
            'accounts/emails/registration_content.txt',
            [user.email],
            subject_data={'site_name': site.name},
            message_data=message_data)

        # redirect to success page
        redirect_url = create_url(
            path=reverse('registration_activation_resend_end'),
            params={'email': user.email})

        return redirect(redirect_url)

    return {'form': form}


@login_required
@render_to('accounts/password_change.html')
def password_change(request):
    """
    Change password
    """
    form = ChangePasswordForm(request.POST or None, request=request)

    if form.is_valid():
        request.user.set_password(request.POST['password'])
        request.user.save()
        return redirect('password_change_end')

    return {'form': form}


@render_to('accounts/password_reset.html')
def password_reset(request):
    """
    Password reset
    """
    form = PasswordResetForm(request.POST or None)

    if form.is_valid():
        # get user
        username_or_email = request.POST['username_or_email']
        if username_or_email.find('@') >= 0:
            user = get_object_or_None(User, email=username_or_email)
        else:
            user = get_object_or_None(User, username=username_or_email)

        # check, if that user already requested password reset
        password_reset_obj = get_object_or_None(PasswordReset, user=user)
        if password_reset_obj:
            password_reset_obj.delete()

        # create password reset object
        pr = PasswordReset(user=user)
        pr.save()

        # get password reset link
        reset_url = pr.get_password_reset_link()

        # send email
        site = get_current_site(request)
        simple_send_email(
            'accounts/emails/password_reset_subject.txt',
            'accounts/emails/password_reset_content.txt',
            [user.email],
            subject_data={'site_name': site.name},
            message_data={
                'site_name': site.name,
                'reset_url': reset_url,
                'username': user.username,
                'reset_timeout': settings.PASSWORD_RESET_TIMEOUT_DAYS
            })
        return redirect('password_reset_end')

    return {'form': form}


@render_to('accounts/password_reset_confirm.html')
def password_reset_confirm(request):
    """
    Confirm password reset
    """

    token = request.GET.get('token')
    password_reset_obj = get_object_or_None(PasswordReset, token=token)
    user = password_reset_obj.user if password_reset_obj else None
    form = NewPasswordForm(request.POST or None)

    # if form is valid, change password and redirect to success page
    if form.is_valid():
        user.set_password(request.POST['password'])
        user.save()
        password_reset_obj.delete()
        return redirect('password_reset_confirm_end')

    if password_reset_obj:
        # check, if reset link doesn't expired
        created_at = password_reset_obj.created_at.replace(tzinfo=None)
        timedelta = datetime.now() - created_at
        if timedelta.days > settings.PASSWORD_RESET_TIMEOUT_DAYS:
            password_reset_obj.delete()
            return redirect('password_reset_failed')
        return {'form': form}
    else:
        return redirect('password_reset_failed')


def is_username_used(request):
    """
    Check, if username is already in database

    :returns: code 200, 'found' or 'not found'
    """
    username = request.POST.get('superCoolData')
    if not get_object_or_None(User, username=username):
        return HttpResponse('not found')
    else:
        return HttpResponse('found')


def is_email_used(request):
    """
    Check, if email is already in use by any user

    :returns: code 200, 'found' or 'not found'
    """
    email = request.POST.get('superCoolData')
    if not get_object_or_None(User, email=email):
        return HttpResponse('not found')
    else:
        return HttpResponse('found')


@login_required
@render_to('accounts/email_change.html')
def email_change(request):
    """
    Show form for email change
    """

    form = ChangeEmailForm(request.POST or None, request=request)
    if form.is_valid():
        email = request.POST.get('email')

        # create activation object
        existed_email_activation = get_object_or_None(
            EmailActivation, user=request.user)
        if existed_email_activation:
            existed_email_activation.delete()
        user_activation = EmailActivation.objects.create(
            user=request.user, email=email)

        # get data for email
        activation_url = user_activation.activation_link
        site = get_current_site(request)
        username = request.user.username

        message_data = {
            'site_name': site.name,
            'activation_url': activation_url,
            'username': username
        }

        simple_send_email(
            'accounts/emails/email_change_subject.txt',
            'accounts/emails/email_change_content.txt',
            [email],
            subject_data={'site_name': site.name},
            message_data=message_data)

        request.session['old_email'] = request.user.email
        request.session['email'] = email
        return redirect('email_change_end')

    return {'form': form}


@render_to('accounts/email_change_end.html')
def email_change_end(request):
    """
    Show page after email change
    """
    email = request.session.get('email')
    old_email = request.session.get('old_email', '')
    email_provider = get_mail_provider_url(email)
    return {
        'email_provider': email_provider,
        'email': request.session.get('email'),
        'old_email': old_email
    }


@login_required
def email_change_confirm(request):
    """
    Activate new email address
    """
    token = request.GET.get('token', '')
    user = request.user

    # check token
    email_activation = get_object_or_None(
        EmailActivation, token=token, user=user)

    if not email_activation:
        return redirect('email_change_confirm_failed')

    else:
        # check, if activation link doesn't expired
        created_at = email_activation.created_at.replace(tzinfo=None)
        timedelta = datetime.now() - created_at
        if timedelta.days > settings.EMAIL_CHANGE_TIMEOUT_DAYS:
            email_activation.delete()
            return redirect('email_change_confirm_failed')

        # activate new email
        user.email = email_activation.email
        user.save()
        email_activation.delete()
        request.session['new_email'] = email_activation.email
        return redirect('email_change_confirm_end')


@login_required
@render_to('accounts/email_change_confirm_end.html')
def email_change_confirm_end(request):
    return {'new_email': request.session.get('new_email', '')}


@login_required
@render_to('accounts/profile_settings.html')
def profile_settings(request):
    form = UserProfileForm(
        request.POST or None, instance=request.user.profile)

    if form.is_valid():
        form.save()
        return redirect(reverse('profile', args=[request.user.username]))

    return {'form': form}
