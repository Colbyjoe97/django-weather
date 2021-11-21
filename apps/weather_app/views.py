from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt, urllib.request, json
from urllib.error import HTTPError


def index(request):
    context={
        'users': User.objects.all(),
    }
    return render(request, 'index.html', context)



def weather(request):
    city = request.POST['city']
    newCity = ""
    for i in range(0, len(city)):
        if city[i] == " ":
            newCity += "+"
        else:
            newCity += city[i]
    if len(newCity) > 0:
        try:
            url = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={newCity}&appid=5ef4efe8fd1e3cf0ddbcee4989acfeda').read()
            data_list = json.loads(url)
                
            temp_c = round(int(data_list['main']['temp']) - 273.1)
            temp_f = round((int(data_list['main']['temp']) - 273.15) * 9/5 + 32)

            request.session['current_city'] = {
                'city': str(data_list['name']),
                "country_code": str(data_list['sys']['country']),
                'temp_c': str(temp_c) + '°C',
                'temp_f': str(temp_f) + '°F',
                'weather_type': str(data_list['weather'][0]['main'])
            }
        except urllib.error.HTTPError as err:
            if err.code:
                messages.error(request, "Please enter a valid city.")
    else:
        messages.error(request, "City is required.")
    return redirect('/')



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

