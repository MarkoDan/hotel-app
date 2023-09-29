from django import forms
from django.contrib.auth.models import User
from .models import Booking

class ProfileForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_guest', 'check_in_date', 'check_out_date']
