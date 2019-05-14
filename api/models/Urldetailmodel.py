from django.db import models


class Urldetails(models.Model):
	url_id = models.CharField(max_length=100,primary_key=True)
	url_nickname= models.CharField(max_length=200,null=True)
	link = models.TextField(null=True)
	sessionid = models.TextField(null=True)
	createddate = models.DateTimeField(null=True)
	status = models.BooleanField(default=1)

	class Meta:
		db_table ='url_details'	
