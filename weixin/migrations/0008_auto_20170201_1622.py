# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 16:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0007_auto_20170131_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='data_device_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin.device'),
        ),
    ]
