# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-15 02:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_tcgroup_main_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tcpickteam',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='tcretailer',
            name='owner',
        ),
    ]