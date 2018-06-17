# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-02 03:41
from __future__ import unicode_literals

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TCUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=11)),
            ],
            options={
                'db_table': 'tc_user',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Buildings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building_name', models.CharField(blank=True, max_length=512, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('holiday', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('business_hour', models.CharField(blank=True, max_length=100, null=True)),
                ('updated_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'buildings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Credits',
            fields=[
                ('credit_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('retailer_id', models.IntegerField(blank=True, null=True)),
                ('ws_name', models.CharField(blank=True, max_length=100, null=True)),
                ('exp_date', models.DateTimeField(blank=True, null=True)),
                ('resolved', models.CharField(blank=True, max_length=10, null=True)),
                ('updated_time', models.DateTimeField()),
                ('created_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'credits',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('notify_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('ws_name', models.CharField(max_length=100)),
                ('retailer_id', models.BigIntegerField()),
                ('prd1', models.CharField(max_length=100)),
                ('prd_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'notify',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrderConfirm',
            fields=[
                ('order_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ws_status', models.CharField(blank=True, max_length=10, null=True)),
                ('pick_status', models.CharField(blank=True, max_length=10, null=True)),
                ('updated_time', models.DateTimeField()),
                ('created_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'order_confirm',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('ws_name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('ws_phone', models.CharField(max_length=12)),
                ('product_name', models.CharField(max_length=50)),
                ('sizencolor', models.CharField(db_column='sizeNcolor', max_length=1024)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('floor', models.CharField(blank=True, default='', max_length=30)),
                ('location', models.CharField(blank=True, default='', max_length=30)),
                ('memo', models.CharField(blank=True, default='', max_length=100)),
                ('updated_time', models.DateTimeField()),
                ('created_time', models.DateTimeField()),
                ('is_deleted', models.CharField(blank=True, max_length=10, null=True)),
                ('notify_id', models.CharField(default='', max_length=100)),
                ('building', models.CharField(default='', max_length=100)),
                ('pickteam_id', models.IntegerField()),
                ('retailer_name', models.CharField(default='', max_length=30)),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('policy_name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('acc_type', models.CharField(max_length=30)),
                ('org_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pickteam',
            fields=[
                ('pickteam_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('pickteam_name', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('business_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('business_type', models.CharField(blank=True, max_length=20, null=True)),
                ('bank_account_num', models.CharField(blank=True, max_length=20, null=True)),
                ('bank', models.CharField(blank=True, max_length=20, null=True)),
                ('bank_holder_name', models.CharField(blank=True, max_length=20, null=True)),
                ('created_time', models.DateTimeField(blank=True, null=True)),
                ('retailer_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'pickteam',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PickteamPickuser',
            fields=[
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('pickteam_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'pickteam_pickuser',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PickupUser',
            fields=[
                ('pickup_user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=512)),
                ('name', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(max_length=12)),
                ('pickteam_id', models.BigIntegerField(blank=True, null=True)),
                ('updated_time', models.DateTimeField(blank=True, null=True)),
                ('account_type', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'pickup_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('retailer_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('retailer_name', models.CharField(max_length=20)),
                ('business_number', models.CharField(max_length=20, unique=True)),
                ('business_type', models.CharField(max_length=20)),
                ('store_type', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=512)),
                ('bank_account_num', models.CharField(max_length=20)),
                ('bank', models.CharField(max_length=20)),
                ('bank_holder_name', models.CharField(max_length=20)),
                ('created_time', models.DateTimeField(auto_now=True, null=True)),
                ('pickteam_id', models.IntegerField()),
                ('main_user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'retailer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RetailerPickteam',
            fields=[
                ('retailer_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('pickteam_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'retailer_pickteam',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RetailUser',
            fields=[
                ('user_idx', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=512)),
                ('name', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(max_length=12)),
                ('updated_time', models.DateTimeField(blank=True, null=True)),
                ('account_type', models.CharField(blank=True, max_length=100, null=True)),
                ('retailer_name', models.CharField(blank=True, default='', max_length=30)),
            ],
            options={
                'db_table': 'retail_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StoreSyles',
            fields=[
                ('style_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('style_en', models.CharField(max_length=1024)),
                ('style_kr', models.CharField(max_length=1024)),
            ],
            options={
                'db_table': 'store_styles',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TCGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=191)),
                ('bank', models.CharField(max_length=191)),
                ('bank_account_number', models.CharField(max_length=191)),
                ('bank_holder_name', models.CharField(max_length=191)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Wholesalers',
            fields=[
                ('ws_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ws_name', models.CharField(max_length=512)),
                ('building_name', models.CharField(max_length=512)),
                ('location', models.CharField(max_length=20)),
                ('product_count', models.IntegerField(blank=True, null=True)),
                ('updated_time', models.DateTimeField(blank=True, null=True)),
                ('floor', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'wholesalers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ws',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ws_name', models.CharField(max_length=30)),
                ('building_name', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=30)),
                ('floor', models.CharField(max_length=30)),
                ('ws_phone', models.CharField(max_length=30)),
                ('updated_time', models.DateTimeField(blank=True, null=True)),
                ('org_id', models.BigIntegerField()),
                ('acc_type', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ws',
                'managed': False,
            },
        ),
    ]