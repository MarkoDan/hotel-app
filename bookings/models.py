# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


class Apartment(models.Model):
    app_label = 'bookings'
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='apartments/')
    maximum_number_of_adults = models.PositiveIntegerField(null=True, blank=True)
    maximum_number_of_kids = models.PositiveIntegerField(null=True, blank=True)
    number_of_rooms = models.PositiveIntegerField(null=True, blank=True)
    number_of_bedrooms = models.PositiveIntegerField(null=True, blank=True)
    number_of_bathrooms = models.PositiveIntegerField(null=True, blank=True)
    size_of_bedrooms = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Bedroom Size (in sqm)")
    size_of_balcony = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Balcony Size (in sqm)")


    #Amenities
    wifi = models.BooleanField(default=True, verbose_name='WIFI')
    tv = models.BooleanField(default=True, verbose_name='TV')
    kitchen = models.BooleanField(default=True, verbose_name='Kitchen')
    size_of_kitchen = models.IntegerField(null=True, blank=True)
    shower = models.BooleanField(default=True, verbose_name='Shower')
    heating = models.BooleanField(default=False, verbose_name='Heating')


class Booking(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_adults = models.PositiveIntegerField(null=True, blank=True)
    number_of_kids = models.PositiveIntegerField(null=True, blank=True)
    booking_date = models.DateField(auto_now_add=True, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    stripe_charge_id = models.CharField(max_length=50, blank=True, null=True)
    idempotency_key = models.CharField(max_length=255, unique=True, null=True, blank=True)

    STATUS_CHOISES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, default='confirmed')
    
    @property
    def user_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"



class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='apartments/')

class MonthlyPricing(models.Model):
    MONTH_CHOICES = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    )

    month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='monthly_prices')


