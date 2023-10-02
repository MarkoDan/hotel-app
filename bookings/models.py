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
    number_of_beds = models.PositiveIntegerField(null=True, blank=True)
    maximix_number_of_guests = models.PositiveIntegerField(null=True, blank=True)

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