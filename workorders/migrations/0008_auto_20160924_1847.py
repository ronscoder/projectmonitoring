# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-24 18:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0007_auto_20160923_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workorders.Project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='workorder',
            name='file',
            field=models.FileField(upload_to='work_orders/%Y/%m/%d/'),
        ),
    ]
