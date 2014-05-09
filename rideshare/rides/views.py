from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from rides.models import Rider, Ride
from rides.forms import UserForm, UserLoginForm, RideForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse

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

def userEvents(request, access_token):
	r = requests.get("https://www.eventbriteapi.com/v3/users/me/orders?token=" + access_token)
	response = json.loads(r.text)

	rider = get_object_or_404(Rider, user=request.user)

	events = {}

	for order in response['orders']:
		event = order['event']
		event_id = event['id']
		name = event['name']['text']

		try:
			ride_to = rider.ride_set.get(event_id=event_id, direction="To Event")
		except Exception, e: ride_to = None

		try:
			ride_from = rider.ride_set.get(event_id=event_id, direction="From Event")
		except Exception, e: ride_from = None


		events[event_id] = [name, ride_to, ride_from]

	return events

def linkRider(request, access_token):
	r = requests.get("https://www.eventbriteapi.com/v3/users/me/?token=" + access_token)
	response = json.loads(r.text)

	rider_id = response['id']

	try:
		rider = Rider.objects.get(user=request.user)
	except Rider.DoesNotExist:
		rider = Rider()

	rider.user = request.user
	rider.eventbrite = rider_id
	rider.access_token = access_token
	rider.save()

@login_required
def eventbrite_permission(request):
    return HttpResponseRedirect("https://www.eventbrite.com/oauth/authorize?response_type=code&client_id=" + CLIENT_KEY)

@login_required
def eventbrite_link(request):
	if request.method == 'GET':
		if 'code' in request.GET:
			access_token = postCode(request.GET['code'])

			if access_token == "error":
				return render(request, 'rides/missing.html', {})

			linkRider(request, access_token)

			return HttpResponseRedirect(reverse('rides:welcome'))

	return HttpResponseRedirect("https://www.eventbrite.com/oauth/authorize?response_type=code&client_id=" + CLIENT_KEY)

def index(request):
	return render(request, 'index.html', {})

def about(request):
        return render(request, 'about.html', {})

def contact(request):
        return render(request, 'contact.html', {})

def get_event_details(request, event_id):
	r = requests.get("https://www.eventbriteapi.com/v3/events/" + event_id + "?token=" + MY_TOKEN)
	response = json.loads(r.text)

	#print response

	if 'error_description' in response:
		return render(request, 'events/invalid.html', {})

	name = response["name"]["text"]
	description = response["description"]["html"]
	organizer = response["organizer"]["name"]
	venue = response["venue"]["name"]
	start = datetime.strptime(response["start"]["local"], "%Y-%m-%dT%H:%M:%S")
	end = datetime.strptime(response["end"]["local"], "%Y-%m-%dT%H:%M:%S")

	return {"name": name, "description": description, "organizer": organizer, "venue": venue, "start": start, "end": end}

@login_required
def welcome(request):
	rider = Rider.objects.get(user=request.user)
	events = userEvents(rider, rider.access_token)
	rides = rider.ride_set.all()

	context = {"events": events, "rider": rider, "rides": rides}
	return render(request, 'rides/profile.html', context)

@login_required
def event_details(request, event_id):
	event = get_event_details(request, event_id)

	rides_to = Ride.objects.filter(event_id=event_id, direction="To Event")
	rides_from = Ride.objects.filter(event_id=event_id, direction="From Event")

	rides = {"rides_to": rides_to, "rides_from": rides_from, "id": event_id}

	context = dict(event.items() + rides.items())	

	return render(request, 'events/details.html', context)

@login_required
def ride_add(request, event_id):
	if request.method == 'POST':
		form = RideForm(request.POST)
		if form.is_valid():
			ride = form.save(commit=False)
			ride.event_id = event_id

			context = get_event_details(request, event_id)
			ride.event_name = context["name"]

			ride.save()
			ride.riders.add(get_object_or_404(Rider, user=request.user))
			return HttpResponseRedirect(reverse('rides:event_details', args=(event_id,)))
	else:
		form = RideForm()
	context = {'form':form}
	return render(request, 'rides/add.html', context)

@login_required
def ride_join(request, ride_id):
	rider = get_object_or_404(Rider, user=request.user)
	ride = get_object_or_404(Ride, id=ride_id)

	if ride.isFull():
		return HttpResponse("This ride is full")

	if rider in ride.riders.all():
		return HttpResponse("You are already taking this ride.")

	ride.riders.add(rider)
	return HttpResponseRedirect(reverse('rides:welcome'))

@login_required
def ride_cancel(request, ride_id):
	rider = get_object_or_404(Rider, user=request.user)
	ride = get_object_or_404(Ride, id=ride_id)

	if not rider in ride.riders.all():
		return HttpResponse("You cannot cancel a ride that you are not taking.")

	ride.riders.remove(rider)
	return HttpResponseRedirect(reverse('rides:welcome'))

@login_required
def ride_details(request, ride_id):
	ride = get_object_or_404(Ride, id=ride_id)
	rider = get_object_or_404(Rider, user=request.user)

	already_joined = (True if rider in ride.riders.all() else False)

	context = {"ride": ride, "already_joined": already_joined}
	return render(request, "rides/details.html", context)

# Based off http://www.tangowithdjango.com/book/chapters/login.html
def user_register(request):
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)

		if user_form.is_valid():
			user = user_form.save()
			password = user.password
			user.set_password(user.password)
			user.save()
			u = authenticate(username=user.username, password=password)
			login(request, u)
			return HttpResponseRedirect(reverse('rides:eventbrite_permission'))

	else:
		user_form = UserForm()

	return render(request, 'register.html', {'form': user_form})

# modified from my 333 project (worked on with Ed Walker)
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.GET and request.GET["next"]:
                    return HttpResponseRedirect(request.GET["next"])
                return HttpResponseRedirect(reverse('rides:welcome'))
        else:        
            form = UserLoginForm()
            form.fields['username'].initial = username
            context = {'form':form, 'title':'Invalid account information'}

    else:
        form = UserLoginForm()
        context = {'form':form, 'title':'Login'}
    return render(request, 'login.html', context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rides:index'))
