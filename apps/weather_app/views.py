from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt, urllib.request, json

# Create your views here.
def index(request):
    # city = request.POST['city']
    url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=sykesville&appid=5ef4efe8fd1e3cf0ddbcee4989acfeda').read()
    data_list = json.loads(url)
    
    temp_c = round(int(data_list['main']['temp']) - 273.1)
    temp_f = round((int(data_list['main']['temp']) - 273.15) * 9/5 + 32)

    data = {
        'city': str(data_list['name']),
        "country_code": str(data_list['sys']['country']),
        'temp_c': str(temp_c) + ' °C',
        'temp_f': str(temp_f) + ' °F',
        'weather_type': str(data_list['weather'][0]['main'])
    }


    context={
        'users': User.objects.all(),
        'weather': data,
        'api': data_list
    }
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html')

def register(request):
    errors = User.objects.registrationValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        hashedPass = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'],email=request.POST['email'],password=hashedPass)
        return redirect("/")