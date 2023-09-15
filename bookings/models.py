# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


class Apartment(models.Model):
    app_label = 'bookings'
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='apartments/')

class Booking(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)