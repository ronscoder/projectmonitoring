from django.db import models

# Create your models here.
from django.db import models

class Project(models.model):
  title = models.CharField('Project Title', max_length=50)
  short_text = models.CharField('Project Description', max_length=200)
  start_date = models.DateTimeField('Tentative start date')
  end_date = models.DateTimeField('Tentative end date')
  actual_start_date = models.DateTimeField('Actual start date')
  actual_end_date = models.DateTimeField('Actual end date')
  project_status = models.CharField('Completion status', max_length=50)

class WorkOrder(models.model):
  order = models.CharField('Order Number', max_length=50)
  order_date = models.DateTimeField('Date of order')
  file = models.FileField(upload_to='files/work_orders/%Y/%m/%d/')
  order_status = models.CharField('Completion status', max_length=50)
  ref_order = models.ForeignKey('self', on_delete=models.CASCADE)
  order_text = models.TextField('Order Summary')

class Division(models.model):
  short_name = models.CharField('Division Name', max_length=20)

class SubDivision(models.model):
  short_name = models.CharField('Division Name', max_length=20)
  ref_division = models.ForeignKey('Division', on_delete=models.CASCADE)

class Package(models.model):
  short_name = models.CharField('Package Name', max_length=20)
  ref_sub_division = models.ForeignKey('SubDivision', on_delete=models.CASCADE)

class Firm(models.model):
  short_name = models.CharField('Firm Name', max_length=20)
  long_name = models.CharField(max_length=200)


class Allocation(models.model):
  order = models.CharField('Order Number', max_length=50)
  order_text = models.TextField('Order Summary')
  order_date = models.DateTimeField('Date of allocation')
  ref_work_order = models.ForeignKey('WorkOrder', on_delete=models.CASCADE)
  ref_allocation = models.ForeignKey('self', on_delete=models.CASCADE)
  ref_package = models.ForeignKey('Package', on_delete=models.CASCADE)

class WorkAssigned(models.model):
  ref_firm = models.ForeignKey('Firm', on_delete=models.CASCADE)
  ref_allocation = models.ForeignKey('Allocation', on_delete=models.CASCADE)
# order status: 1 = open, 2 = closed, 3 = canceled
class DValues(models.model):
  field_name = models.CharField('Field name', max_length=50)
  value = models.CharField('Value', max_length=100)

