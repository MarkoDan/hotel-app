import uuid
from django.shortcuts import get_object_or_404, render, redirect
from bookings.forms import BookingForm, AvailabilityCheckForm
from ..models import Apartment, Booking, User
from django.core.paginator import Paginator
from datetime import date, timedelta, datetime
from django.db.models import Q
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponse
import stripe
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import logging
from django.template.loader import render_to_string
from django.core.mail import send_mail


logger = logging.getLogger(__name__)




def apartments_view(request):
    if request.method == "GET":
        context = fetch_appartments(request)
        
        return render(request, 'bookings/available_apartments.html', context)
    

    
def book_apartment(request):
    apartment = get_object_or_404(Apartment)
    

    #Check user authentication
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in to make a booking. Showing availability only.')
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            number_of_guests = form.cleaned_data['number_of_guests']

            if check_in_date < date.today():
                messages.error(request, 'Check-in date cannot be in the past.')
                context = {'form':form, 'apartment': apartment}
                return render(request, 'bookings/apartment.html', context)
            
            if check_out_date <= check_in_date:
                messages.error(request, 'Check-out date must be after check-in date.')
                context = {'form':form, 'apartment': apartment}
                return render(request, 'bookings/apartment.html', context)
            
            # check if the apartment is already booked
            overlapping_bookings = Booking.objects.filter(
                check_in_date__lt=check_out_date, 
                check_out_date__gt=check_in_date,
                status='confirmed'
            )

            if overlapping_bookings.exists():
                messages.error(request, 'The apartment is already booked for the specified date.')
            elif apartment.maximum_number_of_guests < number_of_guests:
                messages.error(request, 'Exceeded maximum number of guests.')
            else:
                request.session['temp_booking'] = {
                    'apartment_id':apartment.id,
                    'user_id': request.user.id,
                    'check_in_date': check_in_date.strftime('%Y-%m-%d'),
                    'check_out_date': check_out_date.strftime('%Y-%m-%d'),
                    'number_of_guests': number_of_guests,
                    'total_price': str(calculate_price(apartment, check_in_date, check_out_date, number_of_guests))
                }
                return redirect('bookings:start_payment')
    else:
        form = BookingForm()
        
    context = {'form': form, 'apartment': apartment}
    return render(request, 'bookings/apartment.html', context)




def check_availability(request):
    apartment = get_object_or_404(Apartment)

    if request.method == "POST":
        form = AvailabilityCheckForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            print(check_in_date)
            print(check_out_date)

            #Check if the apartment is already booked
            overlapping_bookings = Booking.objects.filter(
                check_in_date__lt=check_out_date, check_out_date__gt=check_in_date
            )

            if overlapping_bookings.exists():
                messages.error(request, 'The apartment is not available for the specified dates.')
            else:
                messages.success(request, 'The apartment is available for the specified dates.')
            
            return redirect('bookings:check_availability')
    else:
        form = AvailabilityCheckForm()

    context = {'form': form, 'apartment': apartment}
    return render(request, 'bookings/apartment.html', context)

        


def booking_success(request):
    return render(request, 'bookings/booking_success.html')

def booking_failed(request):
    return render(request, 'bookings/booking_failed.html')

def display_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/display_bookings.html', {'bookings': bookings})


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



def calculate_price(apartment, check_in_date, check_out_date, number_of_guests):
    
    monthly_price = apartment.monthly_prices.get(month=check_in_date.month)

    days = (check_out_date - check_in_date).days
    return monthly_price.price * days * number_of_guests



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





def send_custom_email(subject, message, to_email_list, from_email=None):
    """
    Sends an email using the Django send_mail function with the Mailjet backend.

    Args:
    - subject (str): Subject of the email.
    - message (str): Plain text body of the email.
    - to_email_list (list): List of recipient email addresses.
    - from_email (str, optional): Sender's email address. Defaults to the DEFAULT_FROM_EMAIL setting.

    Returns:
    - int: Number of successfully sent emails.
    """
    
    # Use the default from_email if none provided
    if not from_email:
        from django.conf import settings
        from_email = settings.DEFAULT_FROM_EMAIL

    # Send the email
    return send_mail(subject, message, from_email, to_email_list)

def start_payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    idempotency_key = str(uuid.uuid4())
    temp_booking = request.session.get('temp_booking')
    if not temp_booking:
        return redirect('bookings:book_apartment') # Redirect back if no temp booking in session
    
    # Create a Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Apartment Booking',
                },
                'unit_amount': int(float(temp_booking['total_price']) * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('bookings:booking_success')),
        cancel_url=request.build_absolute_uri(reverse('bookings:book_apartment')),
        metadata={'temp_booking': json.dumps(temp_booking), 'idempotency_key': idempotency_key},
    )
    
    return redirect(session.url)


class StripeWebhook(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(StripeWebhook, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = 'whsec_c3f099f10c9202c2b15aeae868eb575dc8c0a6e990892fa5970590f7ba3aecf0'

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )

            
        except ValueError:
            #Invalid payload
            return JsonResponse({'status': 'error', 'message': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError:
            #Invalid signature
            return JsonResponse({'status': 'error', 'message': 'Invalid payload'}, status=400)
        
        #Handle the event
        if event.type == 'checkout.session.completed':
            session = event.data.object
            #Handle the checkout session completion
            handle_checkout_session(session)
        
        return JsonResponse({'status': 'success'})




def handle_checkout_session(session):
    try:
        logger.info("handle_checkout_session has been called.")
        temp_booking = json.loads(session.metadata['temp_booking'])
        logger.info(f"Temp booking data: {temp_booking}")
        idempotency_key = session.metadata.get('idempotency_key')
        logger.info(f"Idempotency key: {idempotency_key}")


        if Booking.objects.filter(idempotency_key=idempotency_key).exists():
            logger.info(f"Booking already processed for idempotency key {idempotency_key}")
            return

        #Save booking to DB
        booking = Booking(
            apartment=Apartment.objects.get(id=temp_booking['apartment_id']),
            user=User.objects.get(id=temp_booking['user_id']),
            check_in_date=datetime.strptime(temp_booking['check_in_date'], '%Y-%m-%d').date(),
            check_out_date=datetime.strptime(temp_booking['check_out_date'], '%Y-%m-%d').date(),
            number_of_guests=temp_booking['number_of_guests'],
            total_price=temp_booking['total_price'],
            stripe_charge_id=session.payment_intent,
            idempotency_key=idempotency_key
        )
        booking.save()
        logger.info(f"Booking saved with ID {booking.id}")

        user_email = User.objects.get(id=temp_booking['user_id']).email
        apartment = Apartment.objects.get(id=temp_booking['apartment_id'])
        user = User.objects.get(id=temp_booking['user_id'])
        check_in_date = datetime.strptime(temp_booking['check_in_date'], '%Y-%m-%d').date()
        check_out_date = datetime.strptime(temp_booking['check_out_date'], '%Y-%m-%d').date()
        number_of_guests = temp_booking['number_of_guests']
        total_price = temp_booking['total_price']
        subject = 'Booking Confirmation'
        message = f"""
        Dear {user.first_name},

        We are pleased to inform you that your booking for the apartment has been confirmed.

        Details of your booking:
        - Check-in Date: {check_in_date.strftime('%B %d, %Y')}
        - Check-out Date: {check_out_date.strftime('%B %d, %Y')}
        - Number of Guests: {number_of_guests}
        - Total Price: ${total_price}

        Thank you for choosing us. We are looking forward to hosting you!

        Best regards,
        Your Hotel Team
        """
        send_custom_email(subject,message,[user_email])

    except Exception as e:
        logger.error(f"Error while processing the checkout session: {e}")
    

def cancel_booking(request, booking_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY  
    
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    days_since_booking = (date.today() - booking.booking_date).days
    if days_since_booking <= 30:
    
        if request.method == "POST" and booking.status == "confirmed":

            if booking.stripe_charge_id:
                try:
                    payment_intent = stripe.PaymentIntent.retrieve(booking.stripe_charge_id)
                    latest_charge_id = payment_intent["latest_charge"]
                    
                    # Check if the charge has already been refunded
                    charge = stripe.Charge.retrieve(latest_charge_id)
                    if not charge.refunded:
                        refund = stripe.Refund.create(charge=latest_charge_id)
                        arn = refund.get('acquirer_reference_number', 'N/A')
                    else:
                        messages.error(request, "This charge has already been refunded.")
                        return redirect('bookings:home')

                except Exception as e:
                    messages.error(request, "There was an error processing the refund.")
                    return redirect('bookings:home')

            # Update the booking status
            booking.status = 'cancelled'
            booking.save()

            # Send a confirmation email to the user
            user_email = request.user.email
            email_subject = "Booking Cancellation and Refund"
            email_message = f"""
            Dear {request.user.first_name},
            
            Your booking for {booking.check_in_date} to {booking.check_out_date} has been successfully cancelled.
            
            We have issued a refund for your booking. Below are the refund details:

            - **Payment Status:** Refunded
            - **Acquirer Reference Number (ARN):** {arn}
            - **Expected Settlement Time:** It may take 5-10 business days for funds to settle in your account. Please note that the exact timing can vary depending on your bank.

            It may take a few days for the money to reach your bank account. If you do not see the refund after 10 business days, we recommend contacting your bank with the ARN provided for more details.

            If you have any other questions or concerns, please don't hesitate to contact us.
            Best regards,
            [Your Hotel Name]
            """

            send_custom_email(email_subject, email_message, [user_email])

            messages.success(request, "Booking cancelled and refund issued.")
            return redirect('bookings:display_bookings')
    else:
        messages.error(request, "Bookings can only be cancelled and refunded up to 30 days after the booking date.")
        return redirect('bookings:display_bookings')
    
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})
