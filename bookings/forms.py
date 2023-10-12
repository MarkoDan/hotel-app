from django import forms
from django.contrib.auth.models import User
from .models import Booking
from datetime import date, datetime
class ProfileForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class BookingForm(forms.ModelForm):
    number_of_adults = forms.IntegerField(required=True, min_value=1, max_value=4)
    number_of_kids = forms.IntegerField(required=False, min_value=1, max_value=2)
    check_in_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))
    check_out_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))
    class Meta:
        model = Booking
        fields = ['number_of_adults', 'number_of_kids', 'check_in_date', 'check_out_date']
    
    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        #Check if check_in_date or check_out_date is not provided
        if not check_in_date or not check_out_date:
            raise forms.ValidationError('Both check-in and check-out dates are required.')
        
        #Check if check_in_date is the past
        elif check_in_date < datetime.today().date():
            self.add_error('check_in_date', 'Please select valid check-in date.')
        
        #Check if check_out_date is in the past
        elif check_out_date < datetime.today().date():
            self.add_error('check_out_date', 'Please select valid check-out Date.')
        
        #Check if check_in_date is after or equal to check_out_date
        elif check_in_date >= check_out_date:
            raise forms.ValidationError('Check-out date must be after the check-in date')

        elif check_in_date < datetime.today().date() and check_out_date < datetime.today().date() and check_in_date >= check_out_date:
            raise forms.ValidationError('Invalid dates selected')
        
        return cleaned_data
        


class AvailabilityCheckForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))
    check_out_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        #Check if check_in_date or check_out_date is not provided
        if not check_in_date or not check_out_date:
            raise forms.ValidationError('Both check-in and check-out dates are required.')
        
        #Check if check_in_date is the past
        elif check_in_date < datetime.today().date():
            self.add_error('check_in_date', 'Please select valid check-in date.')
        
        #Check if check_out_date is in the past
        elif check_out_date < datetime.today().date():
            self.add_error('check_out_date', 'Please select valid check-out Date.')
        
        #Check if check_in_date is after or equal to check_out_date
        elif check_in_date >= check_out_date:
            raise forms.ValidationError('Check-out date must be after the check-in date')

        elif check_in_date < datetime.today().date() and check_out_date < datetime.today().date() and check_in_date >= check_out_date:
            raise forms.ValidationError('Invalid dates selected')
        
        return cleaned_data

        
