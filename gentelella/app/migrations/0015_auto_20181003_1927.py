# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-03 10:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_order_pickteam'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pickteam',
            field=models.ForeignKey(db_column='pickteam_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TCPickteam'),
        ),
    ]