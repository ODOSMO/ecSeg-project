# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-25 01:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190525_0148'),
    ]

    operations = [
        migrations.DeleteModel(
            name='database',
        ),
        migrations.DeleteModel(
            name='query',
        ),
    ]
