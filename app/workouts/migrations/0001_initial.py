# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import timedelta.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BestTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'duration', timedelta.fields.TimedeltaField(max_value=None, min_value=None)),
            ],
            options={
                'verbose_name': 'najlepszy czas',
                'verbose_name_plural': 'najlepsze czasy',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance', models.FloatField(unique=True)),
                ('name', models.CharField(max_length=64, verbose_name='Nazwa', blank=True)),
            ],
            options={
                'ordering': ['distance'],
                'verbose_name': 'dystans',
                'verbose_name_plural': 'dystanse',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='Nazwa')),
                ('slug', models.SlugField(unique=True, null=True, blank=True)),
                ('category', models.CharField(max_length=16, verbose_name='Kategoria', choices=[(b'athletic', 'atletyka'), (b'combat', 'sporty walki'), (b'cycling', 'jazda na rowerze'), (b'horsemanship', 'je\u017adziectwo'), (b'other', 'inne'), (b'running', 'bieganie'), (b'team', 'sporty zespo\u0142owe'), (b'tennis', 'tenis i podobne'), (b'walking', 'chodzenie'), (b'water', 'sporty wodne'), (b'winter', 'sporty zimowe')])),
                ('show_distances', models.BooleanField(default=True)),
                ('show_map', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'sport',
                'verbose_name_plural': 'sporty',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='czas utworzenia')),
                ('name', models.CharField(max_length=64, null=True, verbose_name='Nazwa', blank=True)),
                ('notes', models.CharField(max_length=512, null=True, verbose_name='Notatki', blank=True)),
                ('distance', models.FloatField(blank=True, null=True, verbose_name='Dystans', validators=[django.core.validators.MinValueValidator(0)])),
                ('datetime_start', models.DateTimeField(verbose_name='Czas rozpocz\u0119cia')),
                ('datetime_stop', models.DateTimeField(verbose_name='Czas zako\u0144czenia')),
                ('is_active', models.BooleanField(default=True, verbose_name='W\u0142\u0105czony do statystyk')),
                ('sport', models.ForeignKey(verbose_name='Dyscyplina', to='workouts.Sport')),
                ('user', models.ForeignKey(related_name='workouts', verbose_name='U\u017cytkownik', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'trening',
                'verbose_name_plural': 'treningi',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='distance',
            name='only_for',
            field=models.ManyToManyField(help_text='Je\u015bli podane, dystans pojawi si\u0119 wy\u0142\u0105cznie dla danych dyscyplin', to='workouts.Sport', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='besttime',
            name='distance',
            field=models.ForeignKey(to='workouts.Distance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='besttime',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='besttime',
            name='workout',
            field=models.ForeignKey(to='workouts.Workout'),
            preserve_default=True,
        ),
    ]
