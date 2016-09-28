from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from .models import WorkOrder
from django.http import JsonResponse
from django.core import serializers
from django.http import Http404
from workorders.models import *
from django.views.decorators.csrf import csrf_exempt
import csv

@csrf_exempt #not recommended
# Create your views here.
def index(request):
  todo = TODO.objects.all().last()
  todo.task = request.POST.get('task')
  #TODO debugger check 
  #todo = TODO(check = False, task = request.body)
  todo.save()
  #get_object_or_404(Project, pk=id)
  #return render(request, 'workorders/index.html', {'orders':serializers.serialize("json", WorkOrder.objects.all())})
  #return JsonResponse(orders, safe=False)
  #return HttpResponse(serializers.serialize("json", WorkOrder.objects.all()), content_type="text/plain")
  #return HttpResponse(serializers.serialize("json", WorkOrder.objects.all()), content_type="application/json")
  #return JsonResponse(serializers.serialize("json", WorkOrder.objects.all()))
  #return JsonResponse([{'order':'123', 'order_text':'test order'},])
  return JsonResponse({'task':todo.task})
def detail(request, work_order_id):
  try:
    workorder = WorkOrder.objects.get(pk=work_order_id)
  except WorkOrder.DoesNotExist:
    raise Http404("Work Order doesn't exist")
  return render(request,'workorders/detail.html', {'workorder': workorder})

def uploads(request):
  #uploaded work completions
  works = WorkAssigned.objects.all()
  for work in works:
    ltworks = LTWorkExecutionHeader.objects.filter(work_assigned=work)
    for ltwork in ltworks:
      ltwork.package = Allocation.objects.filter(order=work.ref_allocation).first().ref_package
      ltwork.save()
  return HttpResponse('<h1 class="badge">Success</h1>')

def uploads_x(request):
  records = []
  divs = Division.objects.all()
  divs.delete()
  workorders = WorkOrder.objects.all()
  workorders.delete()

  #firms = Firm.objects.all()
  #firms.delete()
  i_alloc = 3000
  with open('workorders/CSV/divs.csv') as csv1:
    reader = csv.DictReader(csv1)
    for row in reader:
      print(row)
      div,created = Division.objects.get_or_create(short_name=row['division'])
      sd,created = div.subdivision_set.get_or_create(short_name=row['sub-division'])
      pk,created = sd.package_set.get_or_create(short_name=row['package'])
      firm,created = Firm.objects.get_or_create(short_name=row['firm'],mobile='123',address='NA')
      order,created = WorkOrder.objects.get_or_create(order='1', order_status='OPEN', project=Project.objects.first(),order_date='2016-09-09')
      work,created = order.workassigned_set.get_or_create(ref_firm=firm, completion_status=row['STATUS'], start_date=row['DAT_ALLOC_POLES'], finish_date='2016-10-30')
      i_alloc = i_alloc + 1
      alloc,created = order.allocation_set.update_or_create(order='%d'%(i_alloc),order_text='Poles', reqd_type ='INITIAL', order_date=row['DAT_ALLOC_POLES'], ref_package = pk)
      i_alloc = i_alloc + 1
      alloc,created = order.allocation_set.update_or_create(order='%d'%(i_alloc),order_text='Cables', reqd_type ='INITIAL', order_date=row['DAT_ALLOC_CABLE'], ref_package = pk)
      i_alloc = i_alloc + 1
     # if not (row['ADD_POLE'] == None or row['ADD_POLE'] == ""):
     #   additional,created = order.allocation_set.update_or_create(order='%d'%(i_alloc),order_text='Poles', reqd_type ='ADDNL', order_date=row['ADD_POLE'], ref_package = pk, ref_allocation = alloc)
     #   i_alloc = i_alloc + 1
     # if not (row['ADD_CABLE'] == None or row['ADD_CABLE']):
     #   additional,created = order.allocation_set.update_or_create(order='%d'%(i_alloc),order_text='Cables', reqd_type ='ADDNL', order_date=row['ADD_CABLE'], ref_package = pk, ref_allocation = alloc)
     #   i_alloc = i_alloc + 1
    #Work assigned
    
      print("XXXXXXXXXXXX"+row['TOTAL'])
      #add dummy DTR's
      for index in range(int(row['TOTAL'])):
        dtr,created = DTR.objects.get_or_create(name="DTR013"+str(i_alloc)+str(index), package=pk, status='OK', model_number='MO'+str(i_alloc)+str(index))
        ltwork = work.ltworkexecutionheader_set.get_or_create(dtr=dtr)  

  return HttpResponse('<h1 class="badge">Success</h1>')





















