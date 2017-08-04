# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-05 11:04
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pluto.models


class Migration(migrations.Migration):

    dependencies = [
        ('pluto', '0003_auto_20170703_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='mate',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='no_image.png', upload_to=pluto.models.user_directory_image_path),
        ),
        migrations.AddField(
            model_name='message',
            name='by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to=settings.AUTH_USER_MODEL),
        ),
    ]
