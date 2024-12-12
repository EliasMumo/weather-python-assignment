from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, WeatherSearchForm
import requests

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'weather/register.html', {'form': form})

@login_required
def weather(request):
    if request.method == 'POST':
        form = WeatherSearchForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            try:
                # Get coordinates from OpenStreetMap
                geocoding_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
                geo_response = requests.get(geocoding_url).json()
                
                if not geo_response:
                    messages.error(request, f"Could not find coordinates for {city}")
                    return render(request, 'weather/weather.html', {'form': form})

                lat = float(geo_response[0]['lat'])
                lon = float(geo_response[0]['lon'])

                # Get weather data from Open-Meteo
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_response = requests.get(weather_url).json()

                weather_data = {
                    'city': city,
                    'temperature': weather_response['current_weather']['temperature'],
                    'windspeed': weather_response['current_weather']['windspeed'],
                }
                return render(request, 'weather/weather.html', 
                            {'form': form, 'weather_data': weather_data})

            except Exception as e:
                messages.error(request, f"Error fetching weather data: {str(e)}")
                return render(request, 'weather/weather.html', {'form': form})
    else:
        form = WeatherSearchForm()
    return render(request, 'weather/weather.html', {'form': form})

def home(request):
    return render(request, 'weather/home.html') 