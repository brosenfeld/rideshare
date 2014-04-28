from django.db import models
from django.contrib.auth.models import User


import datetime

class Rider(models.Model):
	user = models.OneToOneField(User)
	eventbrite = models.PositiveIntegerField()
	access_token = models.CharField(max_length=30)

	def __unicode__(self):
		return self.user.first_name + " " + self.user.last_name + " " + str(self.eventbrite)

class Ride(models.Model):

	direction_choices = (
        (True, "TO"),
        (False, "FROM"),
    )

	event = models.CharField(max_length=20)
	time = models.DateTimeField()
	direction = models.BooleanField(choices=direction_choices)
	location = models.CharField(max_length=50)
	riders = models.ManyToManyField(Rider)

	def __unicode__(self):
		return self.location + " " + str(self.time)