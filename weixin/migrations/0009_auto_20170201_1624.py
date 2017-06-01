# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 16:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0008_auto_20170201_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='data_device_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.device', unique=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_id',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]