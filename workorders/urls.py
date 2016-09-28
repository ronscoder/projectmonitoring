from django.conf.urls import url 
from . import views
from django.contrib import admin


urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^(?P<work_order_id>[0-9]+)/$', views.detail, name='detail'),
  url(r'^uploads/$', views.uploads,name='uploads')
  ]