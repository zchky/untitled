# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 21:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pydrone', '0004_auto_20170126_2148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='test',
            new_name='test1',
        ),
    ]