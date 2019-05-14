from django.contrib import admin
from django.urls import path,include
from api.views import Generatetinyurl,Getlink,Fetchurldetails,Removeurl,Getdetail_via_nickname

urlpatterns = [
		#path('admin/', admin.site.urls),
		path('generate',Generatetinyurl.as_view(),name='generatetinyurl'),
		path('fetchurl/<urlid>',Getlink.as_view(),name='getlink'),
		path('getdetails/<pageno>/<sessionid>',Fetchurldetails.as_view(),name='Fetchurldetails'),
		path('remove',Removeurl.as_view(),name='removeurl'),
		path('getnickname',Getdetail_via_nickname.as_view(),name='nickname'),
	]