# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-15 11:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20181010_1637'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tcorg',
            options={'managed': False, 'verbose_name': 'TC Org', 'verbose_name_plural': 'TC Orgs'},
        ),
        migrations.AlterModelOptions(
            name='tcretailer',
            options={'managed': False, 'verbose_name': 'TC Retailer', 'verbose_name_plural': 'TC Retailers'},
        ),
    ]
