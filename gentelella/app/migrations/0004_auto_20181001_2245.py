# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-01 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20181001_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='tcorg',
            name='account_number',
            field=models.CharField(default='', max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='tcorg',
            name='bank',
            field=models.CharField(default='', max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='tcorg',
            name='bank_account_number',
            field=models.CharField(default='', max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='tcorg',
            name='bank_holder_name',
            field=models.CharField(default='', max_length=191, null=True),
        ),
    ]
