# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-25 09:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20180625_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='WsByUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ws_name', models.CharField(max_length=30)),
                ('building_name', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=30)),
                ('floor', models.CharField(max_length=30)),
                ('ws_phone', models.CharField(max_length=30)),
                ('updated_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': "TCUser's Wholesaler",
                'managed': True,
                'verbose_name_plural': "TCUser's Wholesalers",
                'db_table': 'WsByUser',
            },
        ),
        migrations.RemoveField(
            model_name='wsbyretailer',
            name='retailer',
        ),
        migrations.DeleteModel(
            name='WsByRetailer',
        ),
    ]
