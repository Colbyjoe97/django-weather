from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt, urllib.request, json
from urllib.error import HTTPError

def index(request):
    if 'current_user' in request.session:
        user = User.objects.get(id=request.session['current_user'])
        favorites = user.favorites.all()
        request.session['favorites'] = []
        favorited = False

        if 'current_city' in request.session:
            city = request.session['current_city']['city']
            newCity = ""
            for i in range(0, len(city)):
                if city[i] == " ":
                    newCity += "+"
                else:
                    newCity += city[i]
                    
            for favorite in user.favorites.all():
                if favorite.city == request.session['current_city']['city'] or favorite.city == newCity:
                    favorited = True

        for favorite in favorites:
            url = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={favorite.city}&appid=5ef4efe8fd1e3cf0ddbcee4989acfeda').read()
            data_list = json.loads(url)
                
            temp_c = round(int(data_list['main']['temp']) - 273.1)
            temp_f = round((int(data_list['main']['temp']) - 273.15) * 9/5 + 32)

            city = {
                'city': str(data_list['name']),
                "country_code": str(data_list['sys']['country']),
                'temp_c': str(temp_c) + '°C',
                'temp_f': str(temp_f) + '°F',
                'weather_type': str(data_list['weather'][0]['main']),
                'id': favorite.id
            }
            request.session['favorites'].append(city)

        context={
            'users': User.objects.all(),
            'current_user': user,
            'favorites': request.session['favorites'],
            'favorited': favorited
        }
    else:
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


def favorite(request):
    if 'current_user' in request.session:
        user = User.objects.get(id=request.session['current_user'])
        city = request.POST['city']
        favorited = False
        newCity = ""

        for i in range(0, len(city)):
            if city[i] == " ":
                newCity += "+"
            else:
                newCity += city[i]
                
        for favorite in user.favorites.all():
            if favorite.city == newCity:
                favorited = True

        if favorited == False:
            newCity = Favorite.objects.create(city=newCity)
            user.favorites.add(newCity)
        else:
            user.favorites.remove(Favorite.objects.get(id=request.POST['city_id']))
    else:
        messages.error(request, "You must be logged in to do that!")
    return redirect('/')


def delete(request):
    if request.session['current_user']:
        city = request.POST['city']
        user = User.objects.get(id=request.session['current_user'])
        user.favorites.remove(Favorite.objects.get(id=city))
    return redirect('/')


def login_page(request):
    return render(request, 'login.html')


def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        user = User.objects.filter(email=request.POST['email'])
        request.session['current_user'] = user[0].id
        return redirect('/')


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


def logout(request):
    del request.session['current_user']
    return redirect('/')