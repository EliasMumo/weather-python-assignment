from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class WeatherSearchForm(forms.Form):
    city = forms.CharField(max_length=100, required=True,
                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Enter city name'})) 