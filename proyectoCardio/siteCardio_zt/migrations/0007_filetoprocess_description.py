# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-21 01:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteCardio_zt', '0006_auto_20191013_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='filetoprocess',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
