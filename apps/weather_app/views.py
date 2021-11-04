from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    context={
        'users': User.objects.all()
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