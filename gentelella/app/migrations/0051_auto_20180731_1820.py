# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-31 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_bulkaddwsformat'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulkaddwsformat',
            name='required',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bulkaddwsformat',
            name='format',
            field=models.CharField(default='', max_length=30),
        ),
    ]
