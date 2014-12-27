# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={},
        ),
        migrations.AlterModelOptions(
            name='activitytype',
            options={},
        ),
        migrations.AlterField(
            model_name='activity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='data_json',
            field=annoying.fields.JSONField(default={}),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='related_date',
            field=models.DateField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.ForeignKey(to='activities.ActivityType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activitytype',
            name='description',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activitytype',
            name='label',
            field=models.SlugField(max_length=64),
            preserve_default=True,
        ),
    ]
