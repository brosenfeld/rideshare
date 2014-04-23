from django.db import models
from django.contrib.auth.models import User

import datetime

class City(models.Model):
	name = models.CharField(max_length=15)

	def __unicode__(self):
		return self.name

class Event(models.Model):
	name = models.CharField(max_length=30)
	creator = models.ForeignKey(User)
	city = models.ForeignKey(City)
	date = models.DateTimeField()
	address = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Ride(models.Model):
	event = models.ForeignKey(Event)
	time = models.DateTimeField()
	start = models.CharField(max_length=30)
	end = models.CharField(max_length=30)

	def __unicode__(self):
		return self.start + " " + str(self.time)