from django.db import models

from datetime import date
from datetime import timedelta

# Create your models here.
from django.db import models

STATUS = (
  ('OPEN','Open'),
  ('ONHOLD','On Hold'),
  ('CANCELED', 'canceled'),
  ('CLOSED','Closed'),
  ('NOT_STARTED', 'Not started')
  )

COMPLETION =  (
  ('IN_PROGRESS','In progress'),
  ('COMPLETED','Completed'),
  ('NOT_STARTED', 'Not started')
  )
class Project(models.Model):
  title = models.CharField('Project Title', max_length=50)
  short_text = models.CharField('Project Description', max_length=200, null=True, blank=True)
  start_date = models.DateField('Tentative start date', null=True, blank=True)
  end_date = models.DateField('Tentative end date', null=True, blank=True)
  actual_start_date = models.DateField('Actual start date', null=True, blank=True)
  actual_end_date = models.DateField('Actual end date', null=True, blank=True)
  project_status = models.CharField('Completion status', max_length=50, choices=STATUS)
  def __str__(self):
    return self.title 

class WorkOrder(models.Model):
  order = models.CharField('Order Number', max_length=50)
  order_text = models.TextField('Order Summary',null=True, blank=True)
  order_date = models.DateField('Date of order')
  file = models.FileField(upload_to='work_orders/%Y/%m/%d/')
  order_status = models.CharField('Completion status', max_length=50, choices=STATUS)
  ref_order = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
  def __str__(self):
    return self.order # + ': ' + self.order_text

class Division(models.Model):
  short_name = models.CharField('Division Name', max_length=20)
  def __str__(self):
    return self.short_name

class SubDivision(models.Model):
  short_name = models.CharField('Division Name', max_length=20)
  ref_division = models.ForeignKey('Division', on_delete=models.CASCADE)
  def __str__(self):
    return self.short_name

class Package(models.Model):
  short_name = models.CharField('Package Name', max_length=20)
  ref_sub_division = models.ForeignKey('SubDivision', on_delete=models.CASCADE)
  def __str__(self):
    return self.short_name

class Firm(models.Model):
  short_name = models.CharField('Firm Name', max_length=50)
  long_name = models.CharField(max_length=200, blank=True, null=True)
  def __str__(self):
    return self.short_name


class Allocation(models.Model):
  order = models.CharField('Order Number', max_length=50)
  order_text = models.TextField('Order Summary', null=True, blank=True)
  order_date = models.DateField('Date of allocation')
  ref_work_order = models.ForeignKey('WorkOrder', on_delete=models.CASCADE)
  ref_allocation = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
  ref_package = models.ForeignKey('Package', on_delete=models.CASCADE)

  def __str__(self):
    return self.order # + ': ' + self.order_text

class WorkAssigned(models.Model):
  ref_firm = models.ForeignKey('Firm', on_delete=models.CASCADE)
  ref_allocation = models.ForeignKey('Allocation', on_delete=models.CASCADE)
  completion_status = models.CharField('Completion status', max_length=50, choices=COMPLETION)
  start_date = models.DateField('Expected start date')
  finish_date = models.DateField('Expected date of completion', null=True, blank=True)
  actual_start_date = models.DateField('Actual start date', null=True, blank=True)
  actual_finish_date = models.DateField('Actual date of completion', null=True, blank=True)
  def days_left(self):
    return (self.finish_date - date.today()).days



class WorkProgress(models.Model):
  ref_work_assigned = models.ForeignKey('WorkAssigned', on_delete=models.CASCADE)
  updated_at = models.DateTimeField('Update date', auto_now = True)
  new_deadline = models.DateField('Promised date of completion')
  reason_text =  models.TextField('Reason for delay')



