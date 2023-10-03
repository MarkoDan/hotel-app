# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


class Apartment(models.Model):
    app_label = 'bookings'
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='apartments/')
    number_of_rooms = models.PositiveIntegerField(null=True, blank=True)
    number_of_bedrooms = models.PositiveIntegerField(null=True, blank=True)
    size_of_bedrooms = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Bedroom Size (in sqm)")
    size_of_balcony = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Balcony Size (in sqm)")

    maximix_number_of_guests = models.PositiveIntegerField(null=True, blank=True)

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
    number_of_guests = models.PositiveIntegerField(null=True, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    
    @property
    def user_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"



class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='apartments/')