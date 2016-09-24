# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-23 16:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(max_length=50, verbose_name='Order Number')),
                ('order_text', models.TextField(blank=True, null=True, verbose_name='Order Summary')),
                ('order_date', models.DateTimeField(verbose_name='Date of allocation')),
                ('ref_allocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorders.Allocation')),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=20, verbose_name='Division Name')),
            ],
        ),
        migrations.CreateModel(
            name='Firm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=20, verbose_name='Firm Name')),
                ('long_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=20, verbose_name='Package Name')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Project Title')),
                ('short_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='Project Description')),
                ('start_date', models.DateTimeField(verbose_name='Tentative start date')),
                ('end_date', models.DateTimeField(verbose_name='Tentative end date')),
                ('actual_start_date', models.DateTimeField(verbose_name='Actual start date')),
                ('actual_end_date', models.DateTimeField(verbose_name='Actual end date')),
                ('project_status', models.CharField(choices=[('OPEN', 'Open'), ('ONHOLD', 'On Hold'), ('CANCELED', 'canceled'), ('CLOSED', 'Closed')], max_length=50, verbose_name='Completion status')),
            ],
        ),
        migrations.CreateModel(
            name='SubDivision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=20, verbose_name='Division Name')),
                ('ref_division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorders.Division')),
            ],
        ),
        migrations.CreateModel(
            name='WorkAssigned',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_status', models.CharField(choices=[('IN_PROGRESS', 'In progress'), ('COMPLETED', 'Completed'), ('NOT_STARTED', 'Not started')], max_length=50, verbose_name='Completion status')),
                ('start_date', models.DateTimeField(verbose_name='Expected start date')),
                ('finish_date', models.DateTimeField(verbose_name='Expected date of completion')),
                ('actual_start_date', models.DateTimeField(verbose_name='Actual start date')),
                ('actual_finish_date', models.DateTimeField(verbose_name='Actual date of completion')),
                ('ref_allocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorders.Allocation')),
                ('ref_firm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorders.Firm')),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(max_length=50, verbose_name='Order Number')),
                ('order_text', models.TextField(blank=True, null=True, verbose_name='Order Summary')),
                ('order_date', models.DateTimeField(verbose_name='Date of order')),
                ('file', models.FileField(upload_to='files/work_orders/%Y/%m/%d/')),
                ('order_status', models.CharField(choices=[('OPEN', 'Open'), ('ONHOLD', 'On Hold'), ('CANCELED', 'canceled'), ('CLOSED', 'Closed')], max_length=50, verbose_name='Completion status')),
                ('ref_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorders.WorkOrder')),
            ],
        ),
        migrations.CreateModel(
            name='WorkProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('new_deadline', models.DateTimeField(verbose_name='Promised date of completion')),
                ('reason_text', models.TextField(verbose_name='Reason for delay')),
                ('ref_work_assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorders.WorkAssigned')),
            ],
        ),
        migrations.AddField(
            model_name='package',
            name='ref_sub_division',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorders.SubDivision'),
        ),
        migrations.AddField(
            model_name='allocation',
            name='ref_package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorders.Package'),
        ),
        migrations.AddField(
            model_name='allocation',
            name='ref_work_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorders.WorkOrder'),
        ),
    ]