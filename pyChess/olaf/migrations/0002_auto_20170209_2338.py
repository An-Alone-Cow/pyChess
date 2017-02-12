# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olaf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customemailfield',
            name='email',
            field=models.EmailField(max_length=64),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
    ]