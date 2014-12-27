# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='besttime',
            options={},
        ),
        migrations.AlterModelOptions(
            name='distance',
            options={'ordering': ['distance']},
        ),
        migrations.AlterModelOptions(
            name='sport',
            options={},
        ),
        migrations.AlterModelOptions(
            name='workout',
            options={},
        ),
        migrations.AlterField(
            model_name='distance',
            name='name',
            field=models.CharField(max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distance',
            name='only_for',
            field=models.ManyToManyField(to='workouts.Sport', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sport',
            name='category',
            field=models.CharField(max_length=16, choices=[(b'athletic', b'athletic'), (b'combat', b'combat'), (b'cycling', b'cycling'), (b'horsemanship', b'horsemanship'), (b'other', b'other'), (b'running', b'running'), (b'team', b'team'), (b'tennis', b'tennis'), (b'walking', b'walking'), (b'water', b'water'), (b'winter', b'winter')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sport',
            name='name',
            field=models.CharField(max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workout',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workout',
            name='datetime_start',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workout',
            name='datetime_stop',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workout',
            name='distance',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workout',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workout',
            name='name',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workout',
            name='notes',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workout',
            name='sport',
            field=models.ForeignKey(to='workouts.Sport'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workout',
            name='user',
            field=models.ForeignKey(related_name='workouts', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
