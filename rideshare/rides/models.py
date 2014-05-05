from django.db import models
from django.contrib.auth.models import User


import datetime

class Rider(models.Model):
	user = models.OneToOneField(User)
	eventbrite = models.CharField(max_length=30)
	access_token = models.CharField(max_length=30)

	def __unicode__(self):
		return self.user.first_name + " " + self.user.last_name + " " + str(self.eventbrite)

class Ride(models.Model):

	direction_choices = (
        ("To Event", "To Event"),
        ("From Event", "From Event"),
    )

	event = models.CharField(max_length=20)
	time = models.DateTimeField()
	direction = models.CharField(max_length=10, choices=direction_choices)
	location = models.CharField(max_length=100)
	riders = models.ManyToManyField(Rider)
	comments = models.CharField(max_length=100)
	capacity = models.PositiveIntegerField()

	def __unicode__(self):
		return self.location + " " + str(self.time)

	def isFull(self):
		riders = Rider.objects.filter(ride=self).count()
		return (True if riders >= self.capacity else False)