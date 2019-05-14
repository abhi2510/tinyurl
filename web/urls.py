from django.urls import path,include
from django.contrib import admin
from .views import generateurl,redirecttolink,generateurlredirect,getnicknamdetails

urlpatterns = [
		#path('admin/', admin.site.urls),
		path('generate/<int:page>',generateurl,name='generateurl'),
		path('',generateurlredirect,name='generateurl'),
		path('generate/',generateurlredirect,name='generateurl'),
		path('<id>',redirecttolink,name='redirecttolink'),
		path('generate/<nickname>',getnicknamdetails,name='getnicknamdetails')
	]