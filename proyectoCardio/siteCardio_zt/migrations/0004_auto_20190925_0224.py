# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-25 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteCardio_zt', '0003_regressionlinearmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='regressionlinearmodel',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='regressionlinearmodel',
            name='name',
            field=models.CharField(default='None', max_length=60),
        ),
    ]
