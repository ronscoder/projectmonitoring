# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-25 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0013_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='ltworkexecutionitem',
            name='file',
            field=models.FileField(default=1, upload_to='progress_report/%Y/%m/%d/'),
            preserve_default=False,
        ),
    ]
