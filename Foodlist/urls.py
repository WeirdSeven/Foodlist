"""Foodlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
	path('', views.index),
	path('admin/', admin.site.urls, name = 'admin'),
	path('menu/', include('menu.urls')),
]

admin.site.site_header = '得来奇管理系统'
admin.site.index_title = '数据库管理'
admin.site.site_title = '得来奇管理系统'
