# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-15 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20181015_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='KakaoTemplates',
            fields=[
                ('tmplId', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('org_msg', models.CharField(max_length=255)),
                ('cta', models.CharField(max_length=255)),
            ],
        ),
    ]