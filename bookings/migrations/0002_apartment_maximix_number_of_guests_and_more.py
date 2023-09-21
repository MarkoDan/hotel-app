# Generated by Django 4.1.7 on 2023-09-16 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='maximix_number_of_guests',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='number_of_beds',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='number_of_rooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='number_of_guests',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]