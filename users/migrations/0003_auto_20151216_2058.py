# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 15:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151216_2005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='ampluas',
            new_name='amplua',
        ),
    ]