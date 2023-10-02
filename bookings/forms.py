from django import forms
from django.contrib.auth.models import User
from .models import Booking

class ProfileForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class BookingForm(forms.ModelForm):
    number_of_guests = forms.IntegerField(required=True)
    check_in_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))
    check_out_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))
    class Meta:
        model = Booking
        fields = ['number_of_guests', 'check_in_date', 'check_out_date']

