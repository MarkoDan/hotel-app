# Generated by Django 4.2.5 on 2023-10-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0010_booking_idempotency_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
