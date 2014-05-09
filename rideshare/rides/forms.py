from django import forms
from django.contrib.auth.models import User
from rides.models import Ride

from datetime import datetime, time

hour_choices = (
     (12, 12), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, 10), (11, 11)
)

minute_choices = (
    (00, '00'), (05, '05'), (10, 10), (15, 15), (20, 20), (25, 25), (30, 30), (35, 35), (40, 40), (45, 45), (50, 50), (55, 55), (60, 60)
)

zone_choices =( ('AM', 'AM'), ('AM', 'PM'))

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
    hours = forms.ChoiceField(choices=hour_choices, help_text='ignore')
    minutes = forms.ChoiceField(choices=minute_choices, help_text='ignore')
    zone = forms.ChoiceField(choices=zone_choices, help_text='ignore')
    time = forms.DateField(label='Date')
    #time = forms.TimeField(input_formats = ['%H:%M', '%I:%M%p', '%I:%M %p'] )
    direction = forms.ChoiceField(widget=forms.Select, choices=Ride.direction_choices)
    location = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), max_length=100, initial="Select location with Google Maps")

    class Meta:
        model = Ride
        fields = ('hours', 'minutes', 'zone', 'time', 'direction', 'location', 'comments', 'capacity')

    def clean_time(self):
        date = self.cleaned_data['time']
        time = str(self.cleaned_data['hours']) + ":" + str(self.cleaned_data['minutes']) + " " + self.cleaned_data["zone"]
        time = datetime.strptime(time, '%I:%M %p').time()
        return datetime.combine(date, time)

    def clean_location(self):
        location = self.cleaned_data['location']
        if location == "Select location with Google Maps":
            raise forms.ValidationError("Please select a location")
        return location

