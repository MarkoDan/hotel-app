# Generated by Django 4.2.5 on 2023-10-10 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0013_remove_apartment_maximum_number_of_guests_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='number_of_bathrooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
