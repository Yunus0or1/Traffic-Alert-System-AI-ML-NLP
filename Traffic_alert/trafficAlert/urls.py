from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
import alert.views 

urlpatterns = [

	path('', alert.views.home,name="home"),
	
	url(r'^search_area_func/$', alert.views.search_area_func, name="search_area_func"),
	url(r'^information/$', alert.views.information, name="information"),
]
