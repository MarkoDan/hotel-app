# Generated by Django 4.2.5 on 2023-10-11 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0015_booking_maximum_number_of_guests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='maximum_number_of_guests',
        ),
    ]
