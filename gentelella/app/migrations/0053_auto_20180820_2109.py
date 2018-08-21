# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-20 12:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0052_orderformats_fmt_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderformats',
            name='fmt_color',
            field=models.CharField(blank=True, max_length=10, verbose_name='컬러 포맷'),
        ),
        migrations.AlterField(
            model_name='orderformats',
            name='fmt_datetime',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='날짜'),
        ),
        migrations.AlterField(
            model_name='orderformats',
            name='fmt_request',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='요청사항 포맷'),
        ),
    ]
