# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-09-22 02:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0002_topic2'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Topic2',
        ),
    ]
