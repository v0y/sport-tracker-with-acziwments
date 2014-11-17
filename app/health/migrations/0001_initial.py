# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Health',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('related_date', models.DateField(verbose_name='powi\u0105zana data')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='Waga', validators=[django.core.validators.MinValueValidator(0)])),
                ('fat', models.FloatField(blank=True, null=True, verbose_name='T\u0142uszcz', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('water', models.FloatField(blank=True, null=True, verbose_name='Woda', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('user', models.ForeignKey(related_name='health', verbose_name='U\u017cytkownik', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'stan zdrowia',
                'verbose_name_plural': 'stan zdrowia',
            },
            bases=(models.Model,),
        ),
    ]
