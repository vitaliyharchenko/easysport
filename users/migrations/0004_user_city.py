# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
        ('users', '0003_auto_20151216_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='places.City'),
        ),
    ]
