from django import forms
from django.contrib.auth.models import User

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