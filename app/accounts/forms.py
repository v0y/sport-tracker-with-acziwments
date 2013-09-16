# coding: utf-8

from datetime import date, datetime

from annoying.functions import get_object_or_None
from django import forms
from django.core import validators
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ModelForm, extras

from .models import UserActivation, UserProfile


# -----------------------------------------------------------------------------
# Mixins
# -----------------------------------------------------------------------------

class CheckCurrentPasswordMixin(forms.Form):
    current_password = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Hasło",
        error_messages={'required': u"Podaj hasło", })

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.request.user.check_password(current_password):
            raise forms.ValidationError(u"Podane hasło jest niepoprane")
        return current_password


class EmailMixin(forms.Form):
    email = forms.EmailField(
        max_length=50, required=True, label=u"Email",
        error_messages={'invalid': u"Podaj poprawny adres email",
                        'required': u"Podaj adres email"})

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
                u"Użytkownik o takim adresie email już istnieje")
        return email


class SetNewPasswordFormMixin(forms.Form):
    password = forms.CharField(
        validators=[validators.MinLengthValidator(5)],
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Nowe hasło",
        error_messages={
            'required': u"Podaj hasło",
            'min_length': u"Hasło musi mieć minimum 5 znaków długości"})

    re_password = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Powtórz nowe hasło",
        error_messages={'required': u"Powtórz hasło", })

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError(u"Hasła nie są zgodne")
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
                raise forms.ValidationError(
                    u"Użytkownik o takim adresie email nie istnieje")
        else:
            #username
            user = get_object_or_None(User, username=username_or_email)
            if not user:
                raise forms.ValidationError(
                    u"Użytkownik o takim loginie nie istnieje")

        return username_or_email


# -----------------------------------------------------------------------------
# Forms
# -----------------------------------------------------------------------------

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30, label=u"Login", required=True,
        error_messages={'required': u"Podaj login"})

    password = forms.CharField(
        max_length=30, label=u"Hasło", required=True,
        widget=forms.PasswordInput,
        error_messages={'required': u"Podaj hasło"})

    class Meta:
        name = u"Logowanie"
        button_text = u"Zaloguj się"


class RegistrationForm(EmailMixin):
    username = forms.SlugField(
        validators=[validators.MinLengthValidator(3)],
        max_length=30, required=True, label=u"Login",
        error_messages={
            'required': u"Podaj login",
            'invalid': u"Login może zawierać tylko litery, "
                       u"cyfry, podkreślenie i myślnik",
            'min_length': u"Login musi mieć minimum 3 znaki długości"})

    password = forms.CharField(
        validators=[validators.MinLengthValidator(5)],
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Hasło",
        error_messages={
            'required': u"Podaj hasło",
            'min_length': u"Hasło musi mieć minimum 5 znaków długości"})

    re_password = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Powtórz hasło", error_messages={'required': u"Powtórz hasło"})

    rules = forms.BooleanField(
        required=True, label=u"Akceptuję regulamin",
        error_messages={
            'required': u"Musisz zaakceptować regulamin"})

    class Meta:
        name = u"Rejestracja"
        button_text = u"Zarejestruj się"

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)
        key_order = ['username', 'email', 'password', 're_password', 'rules']
        self.fields.keyOrder = key_order

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError(u"Hasła nie są zgodne")
        return re_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username):
            raise forms.ValidationError(
                u"Użytkownik o takim loginie już istnieje")
        return username


class ResendActivationMailForm(UsernameOrEmailMixin):
    class Meta:
        name = u"Wyślij link aktywacyjny"
        button_text = u"Wyślij link aktywacyjny"

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        user = get_object_or_None(User, username=username_or_email) or \
               get_object_or_None(User, email=username_or_email)

        # check, if account is already activated
        if user and user.is_active:
            raise forms.ValidationError(
                u"Konto jest już aktywne, możesz się zalogować.")

        # check, if old activation link is used
        if user and not get_object_or_None(UserActivation, user=user):
            raise forms.ValidationError(u"Nie możesz aktywować swojego konta")

        return super(ResendActivationMailForm, self).clean_username_or_email()


class ChangePasswordForm(SetNewPasswordFormMixin):
    old_password = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput,
        label=u"Aktualne hasło",
        error_messages={'required': u"Powtórz hasło", })

    class Meta:
        name = u"Zmiana hasła"
        button_text = u"Zmień hasło"

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['old_password', 'password', 're_password']

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.request.user.check_password(old_password):
            raise forms.ValidationError(u"Podane hasło jest niepoprane")
        return old_password


class PasswordResetForm(UsernameOrEmailMixin):
    class Meta:
        name = u"Reset hasła"
        button_text = u"Resetuj hasło"


class NewPasswordForm(SetNewPasswordFormMixin):

    class Meta:
        name = u"Ustawienie nowego hasła"
        button_text = u"Ustaw nowe hasło"


class ChangeEmailForm(CheckCurrentPasswordMixin, EmailMixin):

    class Meta:
        name = u"Zmiana adresu email"
        button_text = u"Zmień adres email"

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['email', 'current_password']


class UserProfileForm(ModelForm):
    dob = forms.DateField(widget=extras.SelectDateWidget(
        years=(lambda y=date.today().year: range(y, y - 100, -1))(),
        attrs={'class': 'form-control dob-field'}))

    class Meta:
        model = UserProfile
        exclude = ('user',)
        name = u"Edycja profilu"
        button_text = u"Zapisz zmiany"

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob and not date.today() > dob:
            raise forms.ValidationError(
                u"Śmieszku, jeszcze się nie urodziłeś xD")
        return dob

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height and not 30 < height < 300:
            raise forms.ValidationError(u"Serio masz %s cm wzrostu?" % height)
        return height
