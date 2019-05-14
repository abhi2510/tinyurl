import requests,json
from django.shortcuts import render,redirect

# Create your views here.

def generateurl(request,page=1):
	if page >0:
		sessionid=check_nd_create_sessionid(request)
		url = 'http://127.0.0.1:8001/api/getdetails/'+str(page)+'/'+sessionid
		response = call_get_request_api(url)
		if response['Status'] == 'Success':
			return render(request,'tinyurldetail.html',{'urldata':response['data'],'sessionid':sessionid,'pageno':page})
		else:
			return render(request,'tinyurldetail.html',{'urldata':[],'sessionid':sessionid,'pageno':page})
	else:
		return redirect('http://127.0.0.1:8001/web/generate/1')
				

def redirecttolink(request,id=None):
	if id:
		url='http://127.0.0.1:8001/api/fetchurl/'+id
		response = call_get_request_api(url)
		if response['Status'] == 'Success':
			return redirect(response['link'])
		else:
			return render(request,'page_not_found.html')	
	else:
		return render(request,'page_not_found.html')	
	
def call_get_request_api(url):
	response = requests.get(url)
	response = response.text
	response = json.loads(response)
	return response

def call_post_request_url(url,payload):
	response = requests.post(url,data=payload)
	response = response.text
	response = json.loads(response)
	return response	

def call_request_api(url,requestdata):
	response = requests.post(url,data=requestdata)
	response = response.text
	response = json.loads(response)
	return response	

def check_nd_create_sessionid(request):
	if not request.session.has_key('session_id'):
		request.session.create()
		request.session['session_id'] = request.session.session_key
		return request.session['session_id']
	else:
		return request.session['session_id']

def generateurlredirect(request):
	return redirect('http://127.0.0.1:8001/web/generate/1')

def getnicknamdetails(request,nickname=None):
	session_id = check_nd_create_sessionid(request)

	url = 'http://127.0.0.1:8001/api/getnickname'
	request_data = json.dumps({"nickname":nickname,"sessionid":session_id})
	payload = {'nickname':request_data}
	response = call_post_request_url(url,payload)
	if response['Status'] == 'Success':
		return render(request,'tinyurldetail.html',{'urldata':response['data'],'sessionid':session_id,'pageno':0})
	else:
		return render(request,'tinyurldetail.html',{'urldata':[],'sessionid':session_id,'pageno':0})



