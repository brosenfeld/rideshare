from django import forms
from django.contrib.auth.models import User
from rides.models import Ride

from datetime import datetime

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

# modified from my 333 project (worked on with Ed Walker)
class UserLoginForm(forms.ModelForm):
    username = forms.CharField(max_length=75, help_text="", label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    class Meta:
        model = User
        fields = ('username', 'password')

class RideForm(forms.ModelForm):
    date = forms.DateField()
    time = forms.TimeField(input_formats = ['%H:%M', '%I:%M%p', '%I:%M %p'] )
    direction = forms.ChoiceField(widget=forms.Select, choices=Ride.direction_choices)
    location = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), max_length=100, initial="Select location with Google Maps")

    class Meta:
        model = Ride
        fields = ('date', 'time', 'direction', 'location', 'comments', 'capacity')

    def clean_time(self):
        time = self.cleaned_data['time']
        date = self.cleaned_data['date']
        return datetime.combine(date, time)

    def clean_location(self):
        location = self.cleaned_data['location']
        if location == "Select location with Google Maps":
            raise forms.ValidationError("Please select a location")
        return location

