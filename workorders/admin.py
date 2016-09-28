from django.contrib import admin

# Register your models here.
from .models import *
#from .models import WorkOrder
#from .models import Allocation
#from .models import Division
#from .models import SubDivision
#from .models import Package
#from .models import Firm
#from .models import WorkAssigned
#from .models import WorkSchedule



admin.site.site_header = 'MSPDCL Internal'

class AllocationInline(admin.StackedInline):
  model = Allocation
  extra = 1
class WorkAssignedInline(admin.StackedInline):
  model = WorkAssigned
  extra = 1

class PackageInline(admin.StackedInline):
  model = Package
  extra = 0
class SubDivisionInline(admin.StackedInline):
  """docstring for SubDivisionInline"""
  model = SubDivision
  extra = 1

class WorkScheduleInline(admin.StackedInline):
  model = WorkSchedule
  extra = 1

class WorkOrderInline(admin.StackedInline):
  """docstring for WorkOrderInline"""
  model = WorkOrder
  extra = 1

class InspectionReportFileInline(admin.StackedInline):
    model = InspectionReportFile
    extra = 0
class InspectionRosterInline(admin.StackedInline):
  model = InspectionRoster
  extra = 1
class InspectionRosterDeltaInline(admin.StackedInline):
  model = InspectionRosterDelta
  extra = 0
class LTWorkExecutionItemInline(admin.StackedInline):
  model = LTWorkExecutionItem
  extra = 0
class LTWorkExecutionHeaderInline(admin.StackedInline):
  model = LTWorkExecutionHeader
  extra = 0
  

class AllocationAdmin(admin.ModelAdmin):
  list_display = ('order','order_text','order_date','ref_package')


class WorkAssignedAdmin(admin.ModelAdmin):
  list_display = ('completion_status','finish_date','days_left','ref_firm','ref_allocation','actual_start_date')
  list_filter = ['completion_status']
  #inlines = [LTWorkExecutionHeaderInline]


class SubDivisionAdmin(admin.ModelAdmin):
  list_display = ('short_name','ref_division')
  inlines = [PackageInline]
  

class DivisionAdmin(admin.ModelAdmin):
  """docstring for DivisionAdmin"""
  inlines = [SubDivisionInline]
    

class WorkOrderAdmin(admin.ModelAdmin):
  list_display = ('project','order_date','order','order_text','order_status','ref_order')
  list_filter = ['project','order_status']
  inlines =[AllocationInline]
  #search_fields = ['short_name']

   

class PackageAdmin(admin.ModelAdmin):
  list_display = ('short_name','ref_sub_division')
  list_filter = ['ref_sub_division']
  search_fields = ['short_name']

class ProjectAdmin(admin.ModelAdmin):
  list_display = ('title','short_text','actual_start_date','end_date','project_status')

class WorkScheduleAdmin(admin.ModelAdmin):
  list_display = ('updated_at','new_deadline','ref_work_assigned') + ('finish_date','reason_text','time_overhead')
  #fields = ['new_deadline','finish_date']
  list_filter = ['ref_work_assigned']
  #search_fields = ['short_name']

class ReportRosterAdmin(admin.ModelAdmin):
  list_display = ('report_as_on','desc_text', 'total_submitted')
  inlines = [LTWorkExecutionItemInline]


class InspectionRosterAdmin(admin.ModelAdmin):
  list_display = ('assignment','inspecting_on','schedule_deviation','inspected_on')
  inlines = [InspectionReportFileInline,InspectionRosterDeltaInline]


class InspectionRosterDeltaAdmin(admin.ModelAdmin):
  list_display = ('assignment','inspecting_on','inspected_on')


class LTWorkExecutionItemAdmin(admin.ModelAdmin):
  list_display = ('header','report_due_date','updated_at')



class LTWorkExecutionHeaderAdmin(admin.ModelAdmin):
 # list_display = ('work_assigned','no_of_dtr','pole_erected','cable_strung','poles_dismantled','cable_dismantled')
  list_display = ('work_assigned','package')
  list_filter=['package']
  inlines = [LTWorkExecutionItemInline]


class TODOAdmin(admin.ModelAdmin):
  list_display = ('task','check')
  list_filter = ['check']

class AssignFieldOfficerAdmin(admin.ModelAdmin):
#  inlines = [PackageInline]
  list_display = ('officer','areas_assigned')


admin.site.register(Project,ProjectAdmin)
admin.site.register(WorkOrder,WorkOrderAdmin)
admin.site.register(Allocation,AllocationAdmin)

admin.site.register(Division,DivisionAdmin)
admin.site.register(SubDivision,SubDivisionAdmin)
admin.site.register(Firm)
admin.site.register(FieldOfficer)
admin.site.register(DTR)
admin.site.register(Feeder)

admin.site.register(Package,PackageAdmin)

admin.site.register(WorkAssigned,WorkAssignedAdmin)
admin.site.register(WorkSchedule,WorkScheduleAdmin)
admin.site.register(LTWorkExecutionHeader,LTWorkExecutionHeaderAdmin)
#admin.site.register(LTWorkExecutionItem,LTWorkExecutionItemAdmin)
admin.site.register(ReportRoster,ReportRosterAdmin)

admin.site.register(AssignFieldOfficer,AssignFieldOfficerAdmin)
admin.site.register(InspectionRoster,InspectionRosterAdmin)
#admin.site.register(InspectionReportFile)
#admin.site.register(InspectionRosterDelta)
admin.site.register(TODO, TODOAdmin)
#admin.site.register(SubText)



