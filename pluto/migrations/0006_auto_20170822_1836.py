# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-22 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pluto', '0005_auto_20170818_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='level',
            name='file',
        ),
        migrations.AlterField(
            model_name='level',
            name='json',
            field=models.TextField(max_length=1024),
        ),
    ]
