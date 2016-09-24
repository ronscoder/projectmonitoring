from django.contrib import admin

# Register your models here.
from .models import Project
from .models import WorkOrder
from .models import Allocation
from .models import Division
from .models import SubDivision
from .models import Package
from .models import Firm
from .models import WorkAssigned
from .models import WorkProgress



admin.site.site_header = 'MSPDCL Internal'

class AllocationAdmin(admin.ModelAdmin):
  list_display = ('order','order_text','order_date','ref_package')

class WorkAssignedAdmin(admin.ModelAdmin):
  list_display = ('ref_firm','ref_allocation','actual_start_date','finish_date','completion_status','days_left')

class SubDivisionAdmin(admin.ModelAdmin):
  list_display = ('short_name','ref_division')

class PackageAdmin(admin.ModelAdmin):
  list_display = ('short_name','ref_sub_division')

class ProjectAdmin(admin.ModelAdmin):
  list_display = ('title','short_text','actual_start_date','end_date','project_status')

admin.site.register(Project,ProjectAdmin)
admin.site.register(WorkOrder)
admin.site.register(Allocation,AllocationAdmin)
admin.site.register(Division)
admin.site.register(SubDivision,SubDivisionAdmin)
admin.site.register(Package,PackageAdmin)
admin.site.register(Firm)
admin.site.register(WorkAssigned,WorkAssignedAdmin)
admin.site.register(WorkProgress)

