from django.shortcuts import get_object_or_404, render, redirect
from ..models import Apartment, Booking
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import Q

def apartments_view(request):
    if request.method == "GET":
        context = fetch_appartments(request)
        
        return render(request, 'bookings/available_apartments.html', context)
    

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
    overlapipping_bookings = Booking.objects.filter(apartment=apartment).filter(
    (Q(check_in_date__lt=check_in) & Q(check_out_date__gt=check_in)) |
    (Q(check_in__lt=check_out) & Q(check_out__date__gt=check_out))
    )
    return overlapipping_bookings.count() == 0


def calculate_total_price(apartment, check_in, check_out):
    number_of_nights = (check_out - check_in).days
    return apartment.price_per_night * number_of_nights
