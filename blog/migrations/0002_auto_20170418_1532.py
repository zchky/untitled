# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-18 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myfield', markdownx.models.MarkdownxField()),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
