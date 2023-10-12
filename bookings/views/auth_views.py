from venv import logger
from django.shortcuts import render, redirect
from ..models import Apartment, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
import logging
from django.contrib.messages import error, success
from django.contrib.auth.decorators import login_required
from bookings.forms import ProfileForm
from django.contrib import messages


def home(request):
    return render(request, 'bookings/home.html')



def login_request(request):
    #If user is already authenticated, redirect them to the home page
    if request.user_isauthenticated:
        return redirect('bookings:home')
    
    #Instantiate the form
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            #Form data is valid
            user = form.get_user()
            login(request, user)
            return redirect('bookings:home')
        else:
            #Display form with errors
            error(request, "Invalid username or password.")



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            user = form.save()

            #Set the backend attribute
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            #Log the user in
            login(request, user)
            success(request, "Registration succesful!")
            return redirect('bookings:home')
        else:
            #If the form is not valid, return the form along with the validation error
            error(request, "Registratio failed. Please check the form for errors.")
            return render(request, 'bookings/register.html', context)
    else:
        form = UserCreationForm()
        return render(request, 'bookings/register.html', {'form': form})


def logout_request(request):
    logout(request)
    return redirect('bookings:home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            success(request, 'Your profile has been updated!')
            return redirect('bookings:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'bookings/profile.html', {'form': form})

def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete() #This deletes the user from database
        messages.success(request, "Your account has been succesfully deleted.")
        logout(request) #Log the user out
        return redirect('bookings:home')
    return render(request, 'bookings/confirm_delete.html')



#Views for rendering the Privacy and Policy page, and Terms & Conditions pages
def privacy_policy(request):
    return render(request, 'bookings/privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'bookings/terms_and_conditions.html')