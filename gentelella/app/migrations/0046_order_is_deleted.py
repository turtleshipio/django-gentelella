# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-10 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_remove_order_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]