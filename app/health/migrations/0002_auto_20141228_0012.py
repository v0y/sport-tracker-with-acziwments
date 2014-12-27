# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='health',
            options={},
        ),
        migrations.AlterField(
            model_name='health',
            name='fat',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='health',
            name='related_date',
            field=models.DateField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='health',
            name='user',
            field=models.ForeignKey(related_name='health', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='health',
            name='water',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='health',
            name='weight',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
    ]
