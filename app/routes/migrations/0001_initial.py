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
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='czas utworzenia')),
                ('start_time', models.DateTimeField(null=True, verbose_name='Czas rozpocz\u0119cia trasy')),
                ('finish_time', models.DateTimeField(null=True, verbose_name='Czas zako\u0144czenia trasy')),
                ('length', models.FloatField(default=0, verbose_name='D\u0142ugo\u015b\u0107 trasy')),
                ('height_up', models.FloatField(default=0, verbose_name='R\xf3\u017cnica wysoko\u015bci w g\xf3r\u0119')),
                ('height_down', models.FloatField(default=0, verbose_name='R\xf3\u017cnica wysoko\u015bci w d\xf3\u0142')),
                ('tracks_json', models.TextField(default=b'[]')),
                ('user', models.ForeignKey(related_name='routes', verbose_name='U\u017cytkownik', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'trasa',
                'verbose_name_plural': 'trasy',
            },
            bases=(models.Model,),
        ),
    ]
