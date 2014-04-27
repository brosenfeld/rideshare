from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import requests
import json

CLIENT_KEY = "BBGT36XVYX5H2RXV7I"
CLIENT_SECRET = "367KMPCJEB7JMNMVIIWGYMRV5WVWRVV7FOEXA66WO7I43CU5I4"

def index(request):
    return HttpResponseRedirect("https://www.eventbrite.com/oauth/authorize?response_type=code&client_id=" + CLIENT_KEY)

def welcome(request):
	if request.method == 'GET':
		if 'code' in request.GET:

			url = "https://www.eventbrite.com/oauth/token"

			data = {
				"code": request.GET['code'],
				"client_secret": CLIENT_SECRET,
				"client_id": CLIENT_KEY,
				"grant_type": 'authorization_code'
			}

			r = requests.post(url, data=data)
			response = json.loads(r.text)

			context = {"access_token": response["access_token"]}
			return render(request, 'rides/index.html', context)
			
		else:
			return render(request, 'rides/missing.html', {})

	return HttpResponseRedirect("https://www.eventbrite.com/oauth/authorize?response_type=code&client_id=" + CLIENT_KEY)

# Create your views here.

#http://localhost:8000/