# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-05 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_tcuser_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tcgroup',
            name='mobile_phone',
            field=models.CharField(max_length=11, null=True),
        ),
    ]