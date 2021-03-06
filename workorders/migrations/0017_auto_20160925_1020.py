# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-25 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0016_remove_workorder_subtext'),
    ]

    operations = [
        migrations.AddField(
            model_name='firm',
            name='address',
            field=models.TextField(default='NA', verbose_name='Present Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='firm',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='firm',
            name='mobile',
            field=models.CharField(default=123434, max_length=30, verbose_name='Contact Number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fieldofficer',
            name='officer',
            field=models.CharField(max_length=100, verbose_name='👤Officer'),
        ),
    ]
