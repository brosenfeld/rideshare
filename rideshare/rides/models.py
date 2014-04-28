from django.db import models

import datetime

class Rider(models.Model):
	first = models.CharField(max_length=20)
	last = models.CharField(max_length=20)
	email = models.CharField(max_length=25)
	eventbrite = models.PositiveIntegerField()

	def __unicode__(self):
		return self.first + " " + self.last + " " + str(self.eventbrite)

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