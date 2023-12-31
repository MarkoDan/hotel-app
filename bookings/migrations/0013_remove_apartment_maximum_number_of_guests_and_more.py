# Generated by Django 4.2.5 on 2023-10-10 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0012_remove_booking_number_of_guests_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='maximum_number_of_guests',
        ),
        migrations.AddField(
            model_name='apartment',
            name='maximum_number_of_adults',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='maximum_number_of_kids',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
