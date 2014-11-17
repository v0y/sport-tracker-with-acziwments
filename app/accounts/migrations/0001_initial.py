# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailActivation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=40, verbose_name='token', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='czas utworzenia')),
                ('email', models.EmailField(max_length=75, verbose_name=b'Adres email')),
                ('user', models.OneToOneField(related_name='email_activation', verbose_name='U\u017cytkownik', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'aktywacja emaila',
                'verbose_name_plural': 'aktywacja emaila',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=40, verbose_name='token', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='czas utworzenia')),
                ('user', models.OneToOneField(related_name='password_reset', verbose_name='U\u017cytkownik', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'reset has\u0142a',
                'verbose_name_plural': 'reset has\u0142a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserActivation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=40, verbose_name='token', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='czas utworzenia')),
                ('user', models.OneToOneField(related_name='activation', verbose_name='U\u017cytkownik', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'aktywacja u\u017cytkownika',
                'verbose_name_plural': 'aktywacje u\u017cytkownik\xf3w',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dob', models.DateField(null=True, verbose_name='Data urodzin', blank=True)),
                ('sex', models.CharField(blank=True, max_length=1, null=True, verbose_name='P\u0142e\u0107', choices=[(b'K', 'Kobieta'), (b'M', 'M\u0119\u017cczyzna')])),
                ('height', models.IntegerField(null=True, verbose_name='Wzrost', blank=True)),
                ('units', models.IntegerField(default=1, verbose_name='Jednostki miary', choices=[(1, 'Metryczne'), (2, 'Imperialne')])),
                ('user', models.OneToOneField(related_name='profile', verbose_name='U\u017cytkownik', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profil u\u017cytkownika',
                'verbose_name_plural': 'profile u\u017cytkownik\xf3w',
            },
            bases=(models.Model,),
        ),
    ]
