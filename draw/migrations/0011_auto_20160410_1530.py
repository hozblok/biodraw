# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-10 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0010_auto_20160410_1250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileowl',
            old_name='original_name',
            new_name='old_name',
        ),
        migrations.AddField(
            model_name='fileowl',
            name='new_name',
            field=models.CharField(default='asd', max_length=241),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fileowl',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fileowl',
            name='path_name',
            field=models.TextField(),
        ),
    ]
