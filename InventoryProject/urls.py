"""
URL configuration for InventoryProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from tools import views

urlpatterns = [
    re_path(r"^$", views.home, name="home"),
    re_path(r"^tools/newtool/$", views.newTool, name="newTool"),
    re_path(r"^supply/newsupply/$", views.newSupply, name="newSupply"),
    re_path(r"^delete/$", views.del_UI, name="delUI"),
    re_path(r"^tools/get/(?P<pk>\w+)/$", views.get_Tool, name="getTool"),
    re_path(r"^supply/get/(?P<pk>\w+)/$", views.get_Supply, name="getSupply"),
    re_path(r"^tools/edit/(?P<pk>\w+)/check/(?P<key>[a-zA-Z0-9-_]+)/(?P<user>\w+)/$", views.check_Tool, name="check_tool"),
    re_path(r"^supply/edit/(?P<pk>\w+)/replen/(?P<key>[a-zA-Z0-9-_]+)/(?P<user>\w+)/$", views.replenish_Supply, name="replenish_supply"),
    re_path(r"^supply/edit/(?P<pk>\w+)/islow/(?P<key>[a-zA-Z0-9-_]+)/$", views.low_Supply, name="low_supply"),
    re_path(r"^tools/del/(?P<pk>[a-zA-Z0-9-_()]+)/(?P<key>[a-zA-Z0-9-_()]+)/$", views.del_Tool, name="del_tool"),
    re_path(r"^supply/del/(?P<pk>\w+)/(?P<key>\w+)/$", views.del_Supply, name="del_supply"),
    path("admin/", admin.site.urls),
]
