# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0005_auto_20170130_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_user',
            name='user',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]