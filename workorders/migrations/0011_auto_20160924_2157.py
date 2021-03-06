# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-24 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0010_auto_20160924_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectionreportfile',
            name='desc_text',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='inspectionroster',
            name='inspected_on',
            field=models.DateField(blank=True, null=True, verbose_name='Inspected on'),
        ),
        migrations.AlterField(
            model_name='inspectionroster',
            name='remark',
            field=models.TextField(blank=True, null=True, verbose_name='Remark'),
        ),
    ]
