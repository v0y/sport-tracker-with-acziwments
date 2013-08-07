# coding: utf-8

from datetime import datetime

from annoying.functions import get_object_or_None
from django import forms
from django.core import validators
from django.conf import settings
from django.contrib.auth.models import User

from .models import UserActivation


class SetNewPasswordFormMixin(forms.Form):
    password = forms.CharField(
        validators=[validators.MinLengthValidator(5)],
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Nowe hasło",
        error_messages={
            'required': u"Podaj hasło",
            'min_length': u"Hasło musi mieć minimum 5 znaków długości"}
    )

    re_password = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Powtórz nowe hasło",
        error_messages={'required': u"Powtórz hasło", }
    )

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError(u"Hasła nie są zgodne")
        return re_password


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30, label=u"Login", required=True,
        error_messages={'required': u"Podaj login"}
    )
    password = forms.CharField(
        max_length=30, label=u"Hasło", required=True,
        widget=forms.PasswordInput,
        error_messages={'required': u"Podaj hasło"}
    )

    class Meta:
        name = u"Logowanie"
        button_text = u"Zaloguj się"


class RegistrationForm(forms.Form):
    username = forms.SlugField(
        validators=[validators.MinLengthValidator(3)],
        max_length=30, required=True, label=u"Login",
        error_messages={
            'required': u"Podaj login",
            'invalid': u"Login może zawierać tylko litery, "\
                       u"cyfry, podkreślenie i myślnik",
            'min_length': u"Login musi mieć minimum 3 znaki długości"
        }
    )

    email = forms.EmailField(
        max_length=50, required=True, label=u"Email",
        error_messages={'invalid': u"Podaj poprawny adres email",
                        'required': u"Podaj adres email"}
    )

    password = forms.CharField(
        validators=[validators.MinLengthValidator(5)],
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Hasło",
        error_messages={
            'required': u"Podaj hasło",
            'min_length': u"Hasło musi mieć minimum 5 znaków długości"}
    )

    re_password = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Powtórz hasło", error_messages={'required': u"Powtórz hasło", }
    )
    rules = forms.BooleanField(
        required=True, label=u"Akceptuję regulamin",
        error_messages={
            'required': u"Musisz zaakceptować regulamin"
        }
    )

    class Meta:
        name = u"Rejestracja"
        button_text = u"Zarejestruj się"

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError(u"Hasła nie są zgodne")
        return re_password

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
            raise forms.ValidationError(
                u"Użytkownik o takim adresie email już istnieje"
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username):
            raise forms.ValidationError(
                u"Użytkownik o takim loginie już istnieje"
            )
        return username


class ResendActivationMailForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=50, label=u"Login lub adres email", required=True
    )

    class Meta:
        name = u"Wyślij link aktywacyjny"
        button_text = u"Wyślij link aktywacyjny"

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        # check, if input in email or username
        if username_or_email.find('@') >= 0:
            # email
            user = get_object_or_None(User, email=username_or_email)
            if not user:
                raise forms.ValidationError(
                    u"Użytkownik o takim adresie email nie istnieje"
                )
        else:
            #username
            user = get_object_or_None(User, username=username_or_email)
            if not user:
                raise forms.ValidationError(
                    u"Użytkownik o takim loginie nie istnieje"
                )

        # check, if account is already activated
        if user.is_active:
            raise forms.ValidationError(
                u"Konto jest już aktywne, możesz się zalogować."
            )

        # check, if old activation link is used
        if not get_object_or_None(UserActivation, user=user):
            raise forms.ValidationError(
                u"Nie możesz aktywować swojego konta"
            )

        return username_or_email


class ChangePasswordForm(SetNewPasswordFormMixin):
    old_password = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Aktualne hasło",
        error_messages={'required': u"Powtórz hasło", }
    )

    class Meta:
        name = u"Zmiana hasła"
        button_text = u"Zmień hasło"

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.fields.keyOrder = ['old_password', 'password', 're_password']
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.request.user.check_password(old_password):
            raise forms.ValidationError(u"Podane hasło jest niepoprane")
        return old_password


class PasswordResetForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=50, label=u"Login lub adres email", required=True
    )

    class Meta:
        name = u"Reset hasła"
        button_text = u"Resetuj hasło"

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        # check, if input in email or username
        if username_or_email.find('@') >= 0:
            # email
            user = get_object_or_None(User, email=username_or_email)
            if not user:
                raise forms.ValidationError(
                    u"Użytkownik o takim adresie email nie istnieje"
                )
        else:
            #username
            user = get_object_or_None(User, username=username_or_email)
            if not user:
                raise forms.ValidationError(
                    u"Użytkownik o takim loginie nie istnieje"
                )

        return username_or_email


class NewPasswordForm(SetNewPasswordFormMixin):

    class Meta:
        name = u"Ustawienie nowego hasła"
        button_text = u"Ustaw nowe hasło"
