# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-22 23:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_squire_theuuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='squire',
            name='admin_approve',
            field=models.BooleanField(default=False),
        ),
    ]
