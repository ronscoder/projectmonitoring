from django.db import models

from datetime import date
from datetime import datetime
from datetime import timedelta



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
REQD_TYPE =  (
  ('INITIAL','Initial allocation'),
  ('ADDNL','Additional'),
  )

class Project(models.Model):
  title = models.CharField('Project Title', max_length=50, unique=True)
  short_text = models.CharField('Project Description', max_length=200, null=True, blank=True)
  start_date = models.DateField('Tentative start date', null=True, blank=True)
  end_date = models.DateField('Tentative end date', null=True, blank=True)
  actual_start_date = models.DateField('Actual start date', null=True, blank=True)
  actual_end_date = models.DateField('Actual end date', null=True, blank=True)
  project_status = models.CharField('Completion status', max_length=50, choices=STATUS)
  def __str__(self):
    return self.title 

class SubText(models.Model):
  type_name = models.CharField('Field type ✋', max_length=10)
  subtext = models.CharField('Subtext', max_length=100) 
  default = models.BooleanField('Default')
  def __str__(self):
    return "%s %c"%(self.subtext,self.default)

#val_subtext = SubText.objects.filter(type_name='ORDER').filter(default=True)

class WorkOrder(models.Model):
  order = models.CharField('Order Number', max_length=50, unique=True)
  #subtext = models.ForeignKey('SubText', default=order, on_delete=models.SET_NULL, blank=True, null=True)
  order_text = models.TextField('Order Summary',null=True, blank=True)
  order_date = models.DateField('Date of order')
  file = models.FileField(upload_to='work_orders/%Y/%m/%d/', null=True,blank=True)
  order_status = models.CharField('Completion status', max_length=50, choices=STATUS)
  ref_order = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
  project =  models.ForeignKey('Project', on_delete=models.CASCADE)
  def __str__(self):
    return self.order # + ': ' + self.order_text

class Division(models.Model):
  short_name = models.CharField('Division Name', max_length=20, unique=True)
  def __str__(self):
    return self.short_name

class SubDivision(models.Model):
  short_name = models.CharField('Sub-division Name', max_length=20, unique=True)
  ref_division = models.ForeignKey('Division', on_delete=models.CASCADE)
  def __str__(self):
    return self.short_name

class Package(models.Model):
  short_name = models.CharField('Package Name', max_length=20, unique=True)
  ref_sub_division = models.ForeignKey('SubDivision', on_delete=models.CASCADE)
  def __str__(self):
    return self.short_name

class Firm(models.Model):
  short_name = models.CharField('Firm Name', max_length=50, unique=True)
  long_name = models.CharField(max_length=200, blank=True, null=True)
  mobile = models.CharField('Contact Number', max_length=30)
  email = models.EmailField('Email', blank=True,null=True)
  address = models.TextField('Present Address')
  def __str__(self):
    return "👤{0:1} 📱{1} 📧{2}".format(self.short_name, self.mobile, self.email)

#Materials Model
#poles - types
#etc...
class Allocation(models.Model):
  order = models.CharField('Order Number', max_length=50, unique=True)
  order_text = models.TextField('Order Summary', null=True, blank=True)
  reqd_type = models.CharField('Requirement type', max_length=50, choices=REQD_TYPE)
  order_date = models.DateField('Date of allocation')
  ref_work_order = models.ForeignKey('WorkOrder', on_delete=models.CASCADE)
  ref_allocation = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
  ref_package = models.ForeignKey('Package', on_delete=models.CASCADE)
  def __str__(self):
    return self.order # + ': ' + self.order_text

#Goods issued
#Poles 7.5m - 10 etc. ref. allocation

class WorkAssigned(models.Model):
  ref_firm = models.ForeignKey('Firm', on_delete=models.CASCADE)
  ref_order = models.ForeignKey('WorkOrder', on_delete=models.CASCADE)
  ref_allocation = models.ForeignKey('Allocation',null=True, blank=True, on_delete=models.SET_NULL)
  completion_status = models.CharField('Completion status', max_length=50, choices=COMPLETION)
  start_date = models.DateField('Expected start date')
  finish_date = models.DateField('Expected date of completion', null=True, blank=True)
  actual_start_date = models.DateField('Actual start date', null=True, blank=True)
  actual_finish_date = models.DateField('Actual date of completion', null=True, blank=True)
  def __str__(self):
    return str(self.ref_firm)#  + ' « ' + str(self.ref_allocation.ref_package)
  def days_left(self):
    if self.actual_finish_date == None and self.finish_date != None:
      return (self.finish_date - date.today()).days
    else: 
      return 'Completed on ' + str(self.actual_finish_date)
  def progress(self):
    return WorkProgress.objects.get(ref_work_assigned = self)



class WorkSchedule(models.Model):
  ref_work_assigned = models.ForeignKey('WorkAssigned', on_delete=models.CASCADE)
  updated_at = models.DateTimeField('Update date', auto_now = True)
  new_deadline = models.DateField('Promised date of completion')
  reason_text =  models.TextField('Reason for delay')
  def finish_date(self):
    return self.ref_work_assigned.finish_date
  #def assigned_firm(self):
  #  return self.ref_work_assigned.ref_firm
  def time_overhead(self):
    if self.ref_work_assigned.actual_finish_date == None:
      return (self.new_deadline - self.ref_work_assigned.finish_date).days
    else: 
      return 'Completed'

class LTWorkExecutionHeader(models.Model):
  unique_together = ("work_assigned", "dtr")
  work_assigned = models.ForeignKey('WorkAssigned', on_delete=models.CASCADE)
  package = models.ForeignKey('Package', on_delete=models.CASCADE, null=True,blank=True)
  dtr = models.ForeignKey('DTR', on_delete=models.CASCADE)
  #no_of_dtr = models.IntegerField('No. of DTRs')
  no_of_poles_2erect = models.IntegerField('No. of poles to be erected', null=True, blank=True)
  length_of_cable_2string =  models.DecimalField('Length of Cable to be strung', decimal_places=2,max_digits=4, null=True, blank=True)
  no_of_poles_2dismantle = models.IntegerField('No. of poles to be dismantled', null=True, blank=True)
  length_of_cable_2dismantle =  models.DecimalField('Length of Cable to be dismantled',decimal_places=2,max_digits=4, null=True, blank=True)
  def __str__(self):
    return str(self.work_assigned)


  def no_of_dtr(self):
    return 10
  def pole_erected(self):
    deltas = []
    items = LTWorkExecutionItem.objects.filter(header=self).order_by('report_due_date')
    for ltwork in items:
      deltas =  deltas + [ltwork.no_of_poles_erected]
    return ' › '.join(str(e) for e in deltas) + " ∑ %d of %d" % (sum(deltas),self.no_of_poles_2erect)
  
  def cable_strung(self):
    deltas = []
    items = LTWorkExecutionItem.objects.filter(header=self).order_by('report_due_date')
    for ltwork in items:
      deltas =  deltas + [ltwork.length_of_cable_strung]
    return ' › '.join(str(e) for e in deltas) + " ∑ %d of %d" % (sum(deltas),self.length_of_cable_2string)

  def poles_dismantled(self):
    deltas = []
    items = LTWorkExecutionItem.objects.filter(header=self).order_by('report_due_date')
    for ltwork in items:
      deltas =  deltas + [ltwork.no_of_poles_dismantled]
    return ' › '.join(str(e) for e in deltas) + " ∑ %d of %d" % (sum(deltas),self.no_of_poles_2dismantle)

  def cable_dismantled(self):
    deltas = []
    items = LTWorkExecutionItem.objects.filter(header=self).order_by('report_due_date')
    for ltwork in items:
      deltas =  deltas + [ltwork.length_of_cable_dismantled]
    return ' › '.join(str(e) for e in deltas) + " ∑ %d of %d" % (sum(deltas),self.length_of_cable_2dismantle)

class ReportRoster(models.Model):
  report_as_on = models.DateField('📅 Report as on', unique=True)
  desc_text = models.CharField('Description', max_length=150)
  def __str__(self):
    return str(self.report_as_on)
  def total_submitted(self):
    submitted = LTWorkExecutionItem.objects.filter(report_due_date=self.report_as_on).count()
    total = ReportRoster.objects.count()
    return "📊 %d of %d" %(submitted,total)

CONDITION =  (
  ('OK','OK'),
  ('NOTOK','Not OK'),
  )

class Feeder(models.Model):
  name = models.CharField('Name of DTR', max_length=100, unique=True)
  status = models.CharField('Status', max_length=50, choices=CONDITION)
  status_txt = models.CharField('Status text', max_length=100, null=True,blank=True)
  about = models.TextField('About the feeder')

class DTR(models.Model):
  name = models.CharField('Name of DTR', max_length=100, unique=True)
  about = models.CharField('About the DTR', max_length=100, null=True,blank=True)
  areas_covered = models.TextField('Areas covered', null=True,blank=True)
  kva = models.IntegerField('Rating in KVA',null=True,blank=True)
  feeder = models.ForeignKey('Feeder', on_delete=models.SET_NULL, null=True,blank=True)
  status = models.CharField('Status', max_length=50, choices=CONDITION)
  status_txt = models.CharField('Status text', max_length=100, null=True,blank=True)
  no_poles = models.IntegerField('Total number of poles', null=True,blank=True)
  length_cable = models.DecimalField('Coverage in length (KM)',decimal_places=2,max_digits=4,null=True,blank=True)
  package = models.ForeignKey('Package', null=True, blank=True, on_delete=models.SET_NULL)
  date_of_manu = models.DateField('Date of manufacture',null=True,blank=True)
  date_of_comm = models.DateField('Date of commission',null=True,blank=True)
  model_number = models.CharField('Model number', max_length=100, unique=True)
  manufacturer = models.CharField('Manufacturer', max_length=100,null=True,blank=True)
  vendor = models.CharField('Vendor', max_length=100,null=True,blank=True)
  #buyer = models.CharField('Buyer', max_length=100,,null=True,blank=True)
  #date_of_buy = models.DateField('Date of buy',null=True,blank=True)
  receipt = models.FileField(upload_to='receipts/DTR/%Y/%m/%d/',null=True,blank=True)
  #deposit work/Internal
  def __str__(self):
    return  str(self.package) + ' – ' + self.name

#TODO: class DTR servicing & cost

class LTWorkExecutionItem(models.Model):
  header = models.ForeignKey('LTWorkExecutionHeader', on_delete=models.CASCADE)
  no_of_poles_erected = models.IntegerField('No. of poles erected')
  length_of_cable_strung =  models.DecimalField('Length of Cable strung',decimal_places=2,max_digits=4)
  no_of_poles_dismantled = models.IntegerField('No. of poles dismantled')
  length_of_cable_dismantled =  models.DecimalField('Length of Cable dismantled',decimal_places=2,max_digits=4)
  updated_at = models.DateTimeField('Update date', auto_now = True)
  report_due_date = models.ForeignKey('ReportRoster', to_field='report_as_on', on_delete=models.CASCADE)
  firm_comment = models.CharField('Comment by firm',max_length=150, null=True, blank=True)
  supervisor_remark = models.CharField('Comment by supervisor',max_length=150, null=True, blank=True)
  internal_remark = models.CharField('Comment by PMU',max_length=150, null=True, blank=True)
  file = models.FileField(upload_to='progress_report/%Y/%m/%d/')
  def __str__(self):
    return "Report %d for %s"%(LTWorkExecutionItem.objects.filter(header=self.header).count(), str(self.header))


class FieldOfficer(models.Model):
  officer = models.CharField('👤Officer', max_length=100, unique=True)
  mobile = models.CharField('Contact Number', max_length=30)
  email = models.EmailField('Email')
  def __str__(self):
    return "👤{0:1} 📱{1} 📧{2}".format(self.officer, self.mobile, self.email)


class AssignFieldOfficer(models.Model):
  officer = models.ForeignKey('FieldOfficer', on_delete=models.CASCADE)
  areas_assigned = models.ForeignKey('Package', on_delete=models.CASCADE)
  def __str__(self):
    return self.officer.officer + " @ " + self.areas_assigned.short_name



class InspectionRoster(models.Model):
  assignment = models.ForeignKey('AssignFieldOfficer', on_delete=models.CASCADE)
  inspecting_on = models.DateField('Inspecting on')
  inspected_on = models.DateField('Inspected on', null=True, blank=True)
  remark = models.CharField('Remark',max_length=200, null=True, blank=True)
  def __str__(self):
    return str(self.assignment) + ' on ' +str(self.inspecting_on)
  def schedule_deviation(self):
    new_schedule = InspectionRosterDelta.objects.filter(inspection_roster=self).last()
    if new_schedule:
      return new_schedule.new_inspection_date
    else: 
      pass


class InspectionReportFile(models.Model):
  file = models.FileField(upload_to='inspections/%Y/%m/%d/')
  inspection_roster = models.ForeignKey('InspectionRoster', on_delete=models.CASCADE)
  desc_text = models.TextField('Description', null=True, blank=True)
  def __str__(self):
    return str(self.inspection_roster)

class InspectionRosterDelta(models.Model):
  inspection_roster = models.ForeignKey('InspectionRoster', on_delete=models.CASCADE)
  new_inspection_date = models.DateField('New Schedule')
  conversation = models.CharField('Cause text',max_length=200)
  def __str__(self):
    return str(self.inspection_roster)


class TODO(models.Model):
  check = models.BooleanField()
  task = models.CharField(max_length=100)




