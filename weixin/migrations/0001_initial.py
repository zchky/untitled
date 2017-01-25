# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='test_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('temperature', models.IntegerField(default=0)),
                ('humidity', models.IntegerField(default=0)),
            ],
        ),
    ]