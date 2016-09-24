from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from .models import WorkOrder
from django.http import JsonResponse
from django.core import serializers
from django.http import Http404

# Create your views here.
def index(request):
  
  #get_object_or_404(Project, pk=id)
  #return render(request, 'workorders/index.html', {'orders':serializers.serialize("json", WorkOrder.objects.all())})
  #return JsonResponse(orders, safe=False)
  #return HttpResponse(serializers.serialize("json", WorkOrder.objects.all()), content_type="text/plain")
  return HttpResponse(serializers.serialize("json", WorkOrder.objects.all()), content_type="application/json")
  #return JsonResponse(serializers.serialize("json", WorkOrder.objects.all()))
  #return JsonResponse([{'order':'123', 'order_text':'test order'},])
def detail(request, work_order_id):
  try:
    workorder = WorkOrder.objects.get(pk=work_order_id)
  except WorkOrder.DoesNotExist:
    raise Http404("Work Order doesn't exist")
  return render(request,'workorders/detail.html', {'workorder': workorder})