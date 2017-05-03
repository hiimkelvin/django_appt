from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_task$', views.add_task),
    url(r'^appointments$', views.appointments),
    url(r'^delete/(?P<id>\d+)?$', views.delete),
    url(r'^appointments/(?P<id>\d+)?$', views.update_appt),
    url(r'^edit/(?P<id>\d+)?$', views.edit),

]
