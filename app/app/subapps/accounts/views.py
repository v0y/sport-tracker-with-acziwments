# coding: utf-8

from datetime import datetime

from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import (ChangePasswordForm, LoginForm, NewPasswordForm,
                    PasswordResetForm, RegistrationForm,
                    ResendActivationMailForm)
from .models import UserActivation, PasswordReset
from app.subapps.shared.helpers import create_url, simple_send_email


@render_to('accounts/login.html')
def login_view(request):
    """login user"""

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
            return {'form': form,
                    'error': u"Nieprawidłowy login lub hasło"}

        # check, if account is activated
        elif not user.is_active:
            return {'form': form,
                    'error': "Twoje konto nie zostało aktywowane"}

        login(request, user)

        return redirect(request.GET.get('next') or
                        getattr(settings, 'REDIRECT_AFTER_LOGIN', '/'))

    return {'form': form}


def logout_view(request):
    """Log out user"""
    logout(request)
    return redirect(getattr(settings, 'REDIRECT_AFTER_LOGOUT', '/'))


@render_to('accounts/registration.html')
def registration(request):
    """Create new account"""

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
        activation_url = u.activation.get_activation_link()

        site = Site.objects.get(pk=settings.SITE_ID)

        # send email
        simple_send_email('accounts/emails/registration_subject.txt',
                          'accounts/emails/registration_content.txt',
                          [email],
                          subject_data={'site_name': site.name},
                          message_data={'site_name': site.name,
                                        'activation_url': activation_url,
                                        'username': username})

        # redirect to end registration page
        redirect_url = create_url(path=reverse('registration_end'),
                                  params={'email': email})
        return redirect(redirect_url)

    return {'form': form}


def registration_activation(request):
    """Activate account and delete used token"""
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
    """Resend activation email"""

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
        activation_url = activation.get_activation_link()

        # send email
        site = Site.objects.get(pk=settings.SITE_ID)
        simple_send_email('accounts/emails/registration_subject.txt',
                          'accounts/emails/registration_content.txt',
                          [user.email],
                          subject_data={'site_name': site.name},
                          message_data={'site_name': site.name,
                                        'activation_url': activation_url,
                                        'username': user.username})

        # redirect to success page
        redirect_url = create_url(
                           path=reverse('registration_activation_resend_end'),
                           params={'email': user.email}
                        )

        return redirect(redirect_url)

    return {'form': form}


@login_required
@render_to('accounts/password_change.html')
def password_change(request):
    """Change password"""
    form = ChangePasswordForm(request.POST or None, request=request)

    if form.is_valid():
        request.user.set_password(request.POST['password'])
        request.user.save()
        return redirect(reverse('password_change_end'))

    return {'form': form}


@render_to('accounts/password_reset.html')
def password_reset(request):
    """Password reset"""
    form = PasswordResetForm(request.POST or None)

    if form.is_valid():
        # get user
        username_or_email = request.POST['username_or_email']
        if username_or_email.find('@') >= 0:
            user = get_object_or_None(User, email=username_or_email)
        else:
            user = get_object_or_None(User, username=username_or_email)

        # check, if that user already requested password reset
        print user
        password_reset = get_object_or_None(PasswordReset, user=user)
        if password_reset:
            password_reset.delete()

        # create password reset object
        pr = PasswordReset(user=user)
        pr.save()

        # get password reset link
        reset_url = pr.get_password_reset_link()

        # send email
        site = Site.objects.get(pk=settings.SITE_ID)
        simple_send_email(
            'accounts/emails/password_reset_subject.txt',
            'accounts/emails/password_reset_content.txt',
            [user.email],
            subject_data={'site_name': site.name},
            message_data={'site_name': site.name,
                          'reset_url': reset_url,
                          'username': user.username,
                          'reset_timeout':
                              settings.PASSWORD_RESET_TIMEOUT_DAYS}
        )
        return redirect(reverse('password_reset_end'))

    return {'form': form}


@render_to('accounts/password_reset_confirm.html')
def password_reset_confirm(request):
    """Confirm password reset"""

    token = request.GET.get('token')
    password_reset = get_object_or_None(PasswordReset, token=token)
    user = password_reset.user if password_reset else None
    form = NewPasswordForm(request.POST or None)

    # if form is valid, change password and redirect to success page
    if form.is_valid():
        user.set_password(request.POST['password'])
        user.save()
        password_reset.delete()
        return redirect(reverse('password_reset_confirm_end'))

    if password_reset:
        # check, if reset link doesn't expired
        created_at = password_reset.created_at.replace(tzinfo=None)
        timedelta = datetime.now() - created_at
        if timedelta.days > settings.PASSWORD_RESET_TIMEOUT_DAYS:
            password_reset.delete()
            return redirect(reverse('password_reset_failed'))
        return {'form': form}
    else:
        return redirect(reverse('password_reset_failed'))


@csrf_exempt
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


@csrf_exempt
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
