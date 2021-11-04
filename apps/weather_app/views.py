from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt, urllib.request, json

# Create your views here.
def index(request):
    # city = request.POST['city']
    url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=sykesville&appid=5ef4efe8fd1e3cf0ddbcee4989acfeda').read()
    data_list = json.loads(url)
    data = {
        'city': 'Sykesville',
        "country_code": str(data_list['sys']['country']),
        'temp': str(data_list['main']['temp']) + '°C',
    }   
    context={
        'users': User.objects.all(),
        'weather': data,
    }
    return render(request, 'index.html', context)

# def weather(request):
#     city = request.POST['city']
#     url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=sykesville&appid=5ef4efe8fd1e3cf0ddbcee4989acfeda').read()
#     data_list = json.loads(url)
#     data = {
#         'city': city,
#         "country_code": str(data_list['sys']['country']),
#         'temp': str(data_list['main']['temp']) + ' °C',
#     }   
#     context={
#         'users': User.objects.all(),
#         'weather': data,
#     }
#     return redirect('/')

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