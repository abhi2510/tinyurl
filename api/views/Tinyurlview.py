import json,datetime,pytz,random
from rest_framework.views import APIView
from django.http import JsonResponse
from api.models import Urldetails
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.db.models import F,Q

class Generatetinyurl(APIView):
	def post(self,request):
		requestadata = request.data.get('urldata')
		requestjson = json.loads(requestadata)

		if requestjson['url']: 
			if not request.session.has_key('session_id'):
				request.session.create()
				request.session['session_id'] = request.session.session_key
			if self.check_url_or_not(requestjson['url']):
				url_id = self.insert_tiny_url(requestjson['url'],requestjson['nickname'],request.session['session_id'])
				final_tiny_url ="http://127.0.0.1:8001/web/"+url_id
				response = {"Status":"Success","Message":"Ok","tinyurl":final_tiny_url,"code":"200"}
			else:
				response = {"Status":"Error","Message":"Invalid Url","code":"300"}
		else:
			response = {"Status":"Error","Message":"Request Parameter Missing","code":"100"}
		return JsonResponse(response)

	def insert_tiny_url(self,url,nickname,sessionid):
		url_id = self.generate_unique_url_id()
		urlobj = Urldetails()
		urlobj.url_nickname = nickname
		urlobj.link = url
		urlobj.sessionid = sessionid
		urlobj.createddate = self.get_current_time()
		urlobj.url_id = url_id
		urlobj.save()

		return url_id

	def check_url_or_not(self,url):
		if 'https://' in url:
			return True
		elif 'http://' in url:
			return True
		else:
			return False

	def get_current_time(self):
		now_date = datetime.datetime.now(pytz.timezone('UTC'))
		now_date = now_date.astimezone(pytz.timezone('Asia/Kolkata'))
		now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
		now_date = datetime.datetime.strptime(now_date,'%Y-%m-%d %H:%M:%S')
		return now_date	

	def generate_unique_url_id(self):
		url_id = ''
		unique_arr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
		for i in range(10):
			nbr = random.randint(0,len(unique_arr)-1)
			url_id +=unique_arr[nbr]
		return url_id	

class Getlink(APIView):
	def get(self,request,urlid):
		try:
			urlobj = Urldetails.objects.get(url_id=urlid)
			response = {"Status":"Success","Message":"Ok","link":urlobj.link,"code":"200"}
		except ObjectDoesNotExist:
			response ={"Status":"Error","Message":"No Such Id Available","code":"100"}	
		return JsonResponse(response)

class Fetchurldetails(APIView):
	def get(self,request,pageno,sessionid):
		if sessionid:
			urlobjcount = Urldetails.objects.filter(sessionid=sessionid,status=1).count()

			no_of_data_display = 5
			limitdata = (int(pageno)-1)*no_of_data_display

			if no_of_data_display*int(pageno) > urlobjcount:
				no_of_data_display = None	

			urlobj = Urldetails.objects.filter(sessionid=sessionid,status=1).values('url_nickname','url_id','link','createddate').order_by('-createddate')[limitdata:no_of_data_display]
			if urlobj:
				url_list =[]
				for urlfetchobj in urlobj:
					fetchdata =self.make_fetch_details(urlfetchobj)
					url_list.append(fetchdata)
				response ={"Status":"Success","Message":"OK","data":url_list,"code":"200"}	
			else:
				response ={"Status":"Error","Message":"No Data Available","code":"100"}	
		else:
			response ={"Status":"Error","Message":"Request Parameter is Missing","code":"100"}		
		return JsonResponse(response)		

	def make_fetch_details(self,urlobj):
		url_arr = {}
		if urlobj:
			url_arr['nickname'] = urlobj['url_nickname']
			url_arr['tinyurl'] = 'http://127.0.0.1:8001/web/'+urlobj['url_id']
			url_arr['urlid'] = urlobj['url_id']
			url_arr['createddate'] = urlobj['createddate']
		return url_arr


class Removeurl(APIView):
	def post(self,request):
		requestdata = request.data.get('delete')
		requestjson = json.loads(requestdata)
		if requestjson['urlid'] and requestjson['sessionid']:
			response=self.check_and_update_status(requestjson['urlid'],requestjson['sessionid'])
		else:
			response = {"Status":"Error","Message":"Request Parameter is Missing","code":"100"}
		return JsonResponse(response)

	def check_and_update_status(self,urlid,sessionid):
		try:
			urlobj = Urldetails.objects.get(
									Q(url_id=urlid) &
									Q(sessionid=sessionid)
								)
			urlobj.status =0
			urlobj.save()
			response ={"Staus":"Success","Message":"Update Successfully","code":"200"}
		except ObjectDoesNotExist:
			response ={"Staus":"Error","Message":"Invalid Id","code":"100"}
		return response			


class Getdetail_via_nickname(APIView):
	def post(self,request):
		requestdata = request.data.get('nickname')
		requestjson = json.loads(requestdata)

		if requestjson['nickname'] and requestjson['sessionid']:
			urlobj = Urldetails.objects.filter(
									Q(url_nickname__contains=requestjson['nickname']) &
									Q(sessionid=requestjson['sessionid'])
								)						
			if urlobj:
				url_list = []
				for urlfetchobj in urlobj:
					fetchdata =self.make_fetch_details(urlfetchobj)
					print(urlfetchobj.url_nickname)
					url_list.append(fetchdata)	
				response ={"Status":"Success","Message":"OK","data":url_list,"code":"200"}
			else:
				response = {"Status":"Error","Message":"Invalid Nickname","code":"100"}		
		else:
			response = {"Status":"Error","Message":"Request Parameter is Missing","code":"100"}
		return JsonResponse(response)	

	def make_fetch_details(self,urlobj):
		url_arr = {}
		if urlobj:
			url_arr['nickname'] = urlobj.url_nickname
			url_arr['tinyurl'] = 'http://127.0.0.1:8001/web/'+urlobj.url_id
			url_arr['urlid'] = urlobj.url_id
			url_arr['createddate'] = urlobj.createddate
		return url_arr							
		
		
		 			
