# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-05 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_tcgroup_mobile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tcgroup',
            name='mobile_phone',
            field=models.CharField(default='01088958454', max_length=11),
        ),
    ]
