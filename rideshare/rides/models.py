from django.db import models
from django.contrib.auth.models import User

import datetime

class Ride(models.Model):

	direction_choices = (
        (True, "TO"),
        (False, "FROM"),
    )

	event = models.CharField(max_length=20)
	time = models.DateTimeField()
	direction = models.BooleanField(choices=direction_choices)
	location = models.CharField(max_length=50)

	def __unicode__(self):
		return self.location + " " + str(self.time)