# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-27 04:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20180626_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='wsbyuser',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wsbyuser',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 27, 13, 39, 55, 710430), null=True),
        ),
    ]