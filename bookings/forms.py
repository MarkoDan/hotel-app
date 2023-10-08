from django import forms
from django.contrib.auth.models import User
from .models import Booking
from datetime import date
class ProfileForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class BookingForm(forms.ModelForm):
    number_of_guests = forms.IntegerField(required=True, min_value=1,)
    check_in_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))
    check_out_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))
    class Meta:
        model = Booking
        fields = ['number_of_guests', 'check_in_date', 'check_out_date']

    def clean_check_in_date(self):
        check_in_date = self.cleaned_data.get('check_in_date')
        if check_in_date < date.today():
            raise forms.ValidationError('Please select a valid check-in date.')
        return check_in_date
    
    def clean_check_out_date(self):
        check_out_date = self.cleaned_data.get('check_out_date')
        if check_out_date < date.today():
            raise forms.ValidationError('Please select valid check-out date.')
        return check_out_date
    
    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        if check_in_date and check_out_date and check_in_date >= check_out_date:
            raise forms.ValidationError('Check-out date must be after the check-in date.')
        

class AvailabilityCheckForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))
    check_out_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))
    
    def clean_check_in_date(self):
        check_in_date = self.cleaned_data.get('check_in_date')
        if check_in_date < date.today():
            raise forms.ValidationError('Please select a valid check-in date.')
        return check_in_date
    
    def clean_check_out_date(self):
        check_out_date = self.cleaned_data.get('check_out_date')
        if check_out_date < date.today():
            raise forms.ValidationError('Please select valid check-out date.')
        return check_out_date
    
    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        if check_in_date and check_out_date and check_in_date >= check_out_date:
           raise forms.ValidationError('Check-out date must be after the check-in date.')
        
