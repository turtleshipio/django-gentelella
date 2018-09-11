# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-11 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_order_parser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='parser',
        ),
        migrations.AddField(
            model_name='tcretailer',
            name='parser',
            field=models.CharField(default='BaseParser', max_length=30),
        ),
    ]
