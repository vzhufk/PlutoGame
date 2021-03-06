# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-18 19:18
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pluto.models


class Migration(migrations.Migration):

    dependencies = [
        ('pluto', '0004_auto_20170705_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('file', models.FileField(upload_to=pluto.models.user_directory_level_path)),
                ('json', models.TextField(max_length=512)),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='by',
        ),
        migrations.RemoveField(
            model_name='message',
            name='to',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
