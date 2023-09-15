
from venv import logger
from django.shortcuts import render, redirect
from .models import Apartment, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
import logging


def home(request):
    return render(request, 'bookings/home.html')



def login_request(request):
    #Handles post request
    if request.method == "POST":
        #Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']

        #Try to check if provided credentials can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            #If user is valid, call login method and login current user
            login(request, user)
            return redirect('bookings:home')
        else:
            return render(request, 'bookings/login.html')
    else:
        return render(request, 'bookings/login.html')




def register(request):
    if request.method == "GET":
        return render(request, 'bookings/register.html')
    elif request.method == "POST":
        #Get user information from request.POST
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        password = request.POST['psw']

        user_exists = False
        try:
            #Check if user already exists
            User.objects.get(username=username)
            user_exists = True
        except:
            #If not, simply log this is a new user
            logger.debug("{} is new user", format(username))

        if not user_exists:
            #Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)

            login(request, user)
            return redirect('bookings:home')
        
        else:
            return render(request, 'bookings/register.html')

