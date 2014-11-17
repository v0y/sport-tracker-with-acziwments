# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='czas utworzenia')),
                ('related_date', models.DateField(verbose_name='powi\u0105zana data')),
                ('data_json', annoying.fields.JSONField(default={}, verbose_name='json templatki')),
            ],
            options={
                'verbose_name': 'aktywno\u015b\u0107',
                'verbose_name_plural': 'aktywno\u015bci',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.SlugField(max_length=64, verbose_name='Etykieta')),
                ('description', models.CharField(max_length=128, null=True, verbose_name='Opis', blank=True)),
            ],
            options={
                'verbose_name': 'typ aktywno\u015bci',
                'verbose_name_plural': 'typy aktywno\u015bci',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='type',
            field=models.ForeignKey(verbose_name='Typ', to='activities.ActivityType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(verbose_name='U\u017cytkownik', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
