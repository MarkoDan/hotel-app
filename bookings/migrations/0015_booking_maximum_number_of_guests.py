# Generated by Django 4.2.5 on 2023-10-11 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0014_apartment_number_of_bathrooms'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='maximum_number_of_guests',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
