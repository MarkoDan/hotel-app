from django.shortcuts import get_object_or_404, render, redirect

from bookings.forms import BookingForm
from ..models import Apartment, Booking
from django.core.paginator import Paginator
from datetime import date, timedelta, datetime
from django.db.models import Q
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse



def apartments_view(request):
    if request.method == "GET":
        context = fetch_appartments(request)
        
        return render(request, 'bookings/available_apartments.html', context)
    
    
# def single_apartment(request):
#     print("Request method", request.method)
#     apartment = get_object_or_404(Apartment)    
#     if request.method == "POST":
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             print('Form is valid')
            
#             with transaction.atomic(): #Start a transaction
#                 if is_apartment_available(apartment, form.cleaned_data['check_in_date'], form.cleaned_data['check_out_date']):
#                     booking = form.save(commit=False)
#                     booking.apartment = apartment
#                     booking.user = request.user
#                     booking.total_price = calculate_total_price(apartment, form.cleaned_data['check_in_date'], form.cleaned_data['check_out_date'])
#                     booking.save()
#                     messages.success(request, 'Booking successfull!')
#                     return redirect('bookings:booking_success')
#                 else:
#                     messages.error(request, 'The apartment is not available for the chosen dates.')
#         else:
#             print('Form is invalid')
#             print(form.errors)
#     else:
#         form = BookingForm()
        
#     context = {'apartment': apartment, 'form': form}
#     return render(request, 'bookings/apartment.html', context)


def single_apartment(request):
    apartment = get_object_or_404(Apartment)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']

            if is_apartment_available(apartment, check_in_date, check_out_date):
                booking = form.save(commit=False)
                booking.apartment = apartment
                booking.user = request.user
                booking.total_price = calculate_total_price(apartment, check_in_date, check_out_date)
                booking.save()
                messages.success(request, 'Booking succesful!')
                return redirect('bookings:booking_success')
            else:
                messages.error(request, 'There was an error with your submission. Please check the details and try again.')
    else:
        form = BookingForm()
        
    context = {
        'apartment': apartment,
        'form': form
    }

    return render(request, 'bookings/apartment.html', context)

    
    

def booking_success(request):
    return render(request, 'bookings/booking_success.html')


def apartment_detail(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    context = {'apartment': apartment}
    return render(request, 'bookings/apartment_detail.html', context)


def fetch_appartments(request, items_per_page=10):
    context = {}
    
    sort_order = request.GET.get('sort', 'asc') # Default to ascending
    
    if sort_order == 'asc':
        apartments_list = Apartment.objects.all().order_by('price_per_night')
    else:
        apartments_list = Apartment.objects.all().order_by('-price_per_night')
    
    paginator = Paginator(apartments_list, items_per_page)
    page = request.GET.get('page')
    apartments = paginator.get_page(page)
    
    context['apartments'] = apartments
    return context


def is_apartment_available(apartment, check_in, check_out):
    overlapping_bookings = Booking.objects.filter(apartment=apartment).filter(
        (Q(check_in_date__lt=check_in) & Q(check_out_date__gt=check_in)) |
        (Q(check_in_date__lt=check_out) & Q(check_out_date__gt=check_out)) |
        (Q(check_in_date=check_out)) |
        (Q(check_out_date=check_in))
    )
    return overlapping_bookings.count() == 0



def calculate_total_price(apartment, check_in, check_out):
    number_of_nights = (check_out - check_in).days
    return apartment.price_per_night * number_of_nights


def apartment_availability(request):
    
    #Get all bookings
    bookings = Booking.objects.all()
    
    #Dictionaries to hold bookings and availability
    booked_dates = {}
    available_dates = {}
    
    
    #Check every day for the next 30 days
    for day in (date.today() + timedelta(n) for n in range(30)):
        booked_apartments = [b.apartment for b in bookings if b.check_in_date <= day <= b.check_out_date]
        available_apartments = Apartment.objects.exclude(id__in=[a.id for a in booked_apartments])
        
        booked_dates[day] = booked_apartments
        available_dates[day] = available_apartments
        
    return render(request, 'path_to_template.html', {
        'booked_dates': booked_dates,
        'available_dates': available_dates,
    })


def availability_result(request, available):
    context = {'available': available}
    return render(request, 'bookings/availability_result.html', context)

    

def is_apartment_available_for_dates(apartment, check_in, check_out):
    # Logic from the single_apartment function
    return is_apartment_available(apartment, check_in, check_out)

def check_availability(request):
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    print('Check-in:', check_in)
    print('Check-out:',check_out)

    apartment = Apartment.objects.first()

    date_format = "%Y-%m-%d"  # Adjust this according to the format sent from the frontend
    check_in_date = datetime.strptime(check_in, date_format).date() if check_in else None
    check_out_date = datetime.strptime(check_out, date_format).date() if check_out else None
    print(check_in_date)
    print(check_out_date)

    if is_apartment_available_for_dates(apartment, check_in_date, check_out_date):
        return redirect('bookings:availability_result', available="True")
    else:
        return redirect('bookings:availability_result', available="False")


