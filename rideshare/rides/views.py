from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rides.models import Rider, Ride

import requests
import json
from datetime import datetime

CLIENT_KEY = "BBGT36XVYX5H2RXV7I"
CLIENT_SECRET = "367KMPCJEB7JMNMVIIWGYMRV5WVWRVV7FOEXA66WO7I43CU5I4"
MY_TOKEN = "6J5TDH6BJRP4BKARHCMJ"

def postCode(code):
	url = "https://www.eventbrite.com/oauth/token"

	data = {
		"code": code,
		"client_secret": CLIENT_SECRET,
		"client_id": CLIENT_KEY,
		"grant_type": 'authorization_code'
	}

	r = requests.post(url, data=data)
	response = json.loads(r.text)

	if "error_description" in response:
		return "error"

	return response["access_token"]

def userEvents(access_token):
	r = requests.get("https://www.eventbriteapi.com/v3/users/me/orders?token=" + access_token)
	response = json.loads(r.text)

	events = {}

	for order in response['orders']:
		event = order['event']
		event_id = event['id']
		name = event['name']['text']
		events[event_id] = name

	return events

def getRider(access_token):
	r = requests.get("https://www.eventbriteapi.com/v3/users/me/?token=" + access_token)
	response = json.loads(r.text)

	rider_id = response['id']

	try:
		rider = Rider.objects.get(eventbrite=rider_id)
	except Rider.DoesNotExist:
		rider = Rider()
		rider.first = response['first_name']
		rider.last = response['last_name']
		rider.email = response['emails'][0]['email']
		rider.eventbrite = int(response['id'])
		rider.save()

	return rider

def index(request):
    return HttpResponseRedirect("https://www.eventbrite.com/oauth/authorize?response_type=code&client_id=" + CLIENT_KEY)

def welcome(request):
	if request.method == 'GET':
		if 'code' in request.GET:
			access_token = postCode(request.GET['code'])

			if access_token == "error":
				return render(request, 'rides/missing.html', {})

			rider = getRider(access_token)
			events = userEvents(access_token)

			context = {"events": events, "rider": rider}
			return render(request, 'rides/index.html', context)

		else:
			return render(request, 'rides/missing.html', {})

	return HttpResponseRedirect("https://www.eventbrite.com/oauth/authorize?response_type=code&client_id=" + CLIENT_KEY)

def event_details(request, event_id):
	r = requests.get("https://www.eventbriteapi.com/v3/events/" + event_id + "?token=" + MY_TOKEN)
	response = json.loads(r.text)

	if 'error_description' in response:
		return render(request, 'events/invalid.html', {})

	name = response["name"]["text"]
	description = response["description"]["html"]
	organizer = response["organizer"]["name"]
	venue = response["venue"]["name"]
	start = datetime.strptime(response["start"]["local"], "%Y-%m-%dT%H:%M:%S")
	end = datetime.strptime(response["end"]["local"], "%Y-%m-%dT%H:%M:%S")

	rides = Ride.objects.filter(event=event_id)

	context = {"name": name, "description": description, "organizer": organizer, "venue": venue, "start": start, "end": end, "rides": rides}

	return render(request, 'events/details.html', context)
