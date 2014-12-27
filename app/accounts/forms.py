# coding: utf-8

from datetime import date, datetime

from annoying.functions import get_object_or_None
from django import forms
from django.core import validators
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ModelForm

from app.shared.forms import SelectDateWidgetWithNone
from .models import (
    UserActivation,
    UserProfile,
)


# -----------------------------------------------------------------------------
# Mixins
# -----------------------------------------------------------------------------

class CheckCurrentPasswordMixin(forms.Form):
    current_password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput,
        label='Password'
    )

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.request.user.check_password(current_password):
            raise forms.ValidationError('Password is incorrect')
        return current_password


class EmailMixin(forms.Form):
    email = forms.EmailField(
        max_length=50, required=True
        # error_messages={
        #     'invalid': 'Enter a valid email address',
        #     'required': 'Enter email address'
        # }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # get activation objects for this email
        activation = get_object_or_None(UserActivation, user__email=email)
        # check if activation time has expired
        if activation:
            created_at = activation.created_at.replace(tzinfo=None)
            timedelta = datetime.now() - created_at
            if timedelta.days > settings.ACCOUNT_ACTIVATION_DAYS:
                user = activation.user
                activation.delete()
                user.delete()
        if email and User.objects.filter(email=email):
            raise forms.ValidationError('This email is already taken.')
        return email


class SetNewPasswordFormMixin(forms.Form):
    password = forms.CharField(
        validators=[validators.MinLengthValidator(5)],
        max_length=30,
        required=True,
        widget=forms.PasswordInput,
        label='New password',
        error_messages={
            'min_length': 'The password must be at least 5 characters long.'
        }
    )

    re_password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput,
        label='Retype new password',
    )

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError('Passwords doesn\'t match')
        return re_password


class UsernameOrEmailMixin(forms.Form):
    username_or_email = forms.CharField(
        max_length=50, label=u"Login lub adres email", required=True)

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        # check, if input in email or username
        if username_or_email.find('@') >= 0:
            # email
            user = get_object_or_None(User, email=username_or_email)
            if not user:
                raise forms.ValidationError('This email is already taken.')
        else:
            # username
            user = get_object_or_None(User, username=username_or_email)
            if not user:
                raise forms.ValidationError(
                    'User with this username does\'t exists.')

        return username_or_email


# -----------------------------------------------------------------------------
# Forms
# -----------------------------------------------------------------------------

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput,
    )

    class Meta:
        name = 'Sign up'
        button_text = 'Sign up'


class RegistrationForm(EmailMixin):
    username = forms.SlugField(
        validators=[validators.MinLengthValidator(3)],
        max_length=30,
        required=True,
        label='Username',
        error_messages={
            'min_length': 'Username is too short (at least 3 chars).'
        },
    )
    password = forms.CharField(
        validators=[validators.MinLengthValidator(5)],
        max_length=30,
        required=True,
        widget=forms.PasswordInput,
        error_messages={
            'invalid': 'Username can only contain letters, '
                       'numbers and signs _ + @ .-',
            'min_length': 'Password is too short (at least 5 chars).'
        },
    )
    re_password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput,
        label='Retype password',
    )
    rules = forms.BooleanField(required=True, label='I accept the terms')

    class Meta:
        name = 'Registration'
        button_text = 'Register'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)
        key_order = ['username', 'email', 'password', 're_password', 'rules']
        self.fields.keyOrder = key_order

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError('Passwords doesn\'t match')
        return re_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username):
            raise forms.ValidationError(
                'This username is already taken.')
        return username


class ResendActivationMailForm(UsernameOrEmailMixin):
    class Meta:
        name = 'Send activation link'
        button_text = 'Send activation link'

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        user = get_object_or_None(User, username=username_or_email) or \
               get_object_or_None(User, email=username_or_email)

        # check, if account is already activated
        if user and user.is_active:
            raise forms.ValidationError('Account is already activated')

        # check, if old activation link is used
        if user and not get_object_or_None(UserActivation, user=user):
            raise forms.ValidationError('Activation link is incorrect')

        return super(ResendActivationMailForm, self).clean_username_or_email()


class ChangePasswordForm(SetNewPasswordFormMixin):
    old_password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput,
        label='Current password',
    )

    class Meta:
        name = 'Password change'
        button_text = 'Change password'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['old_password', 'password', 're_password']

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.request.user.check_password(old_password):
            raise forms.ValidationError('Password is incorrect.')
        return old_password


class PasswordResetForm(UsernameOrEmailMixin):
    class Meta:
        name = 'Password reset'
        button_text = 'Reset Password'


class NewPasswordForm(SetNewPasswordFormMixin):

    class Meta:
        name = 'Password change'
        button_text = 'Change password'


class ChangeEmailForm(CheckCurrentPasswordMixin, EmailMixin):

    class Meta:
        name = 'Email address change'
        button_text = 'Change email'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['email', 'current_password']


class UserProfileForm(ModelForm):
    dob = forms.DateField(widget=SelectDateWidgetWithNone(
        years=(lambda y=date.today().year: range(y, y - 150, -1))(),
        attrs={'class': 'form-control dob-field'}),
        required=False,
        label=u"Date of birth",
    )

    class Meta:
        model = UserProfile
        exclude = ('user',)
        name = 'Profile settings'
        button_text = 'Save'

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob and not date.today() > dob:
            raise forms.ValidationError(
                'Are you time traveller, or something?')
        return dob

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height and not 30 < height < 300:
            raise forms.ValidationError('Are you really %s cm tall?' % height)
        return height
