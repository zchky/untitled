# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 14:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_markdown'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Archive_name', models.CharField(default='others', max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='Archive',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.Archive'),
            preserve_default=False,
        ),
    ]
