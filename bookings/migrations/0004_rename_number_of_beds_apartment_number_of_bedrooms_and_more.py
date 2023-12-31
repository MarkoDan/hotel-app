# Generated by Django 4.2.5 on 2023-10-03 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_apartmentimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apartment',
            old_name='number_of_beds',
            new_name='number_of_bedrooms',
        ),
        migrations.AddField(
            model_name='apartment',
            name='heating',
            field=models.BooleanField(default=False, verbose_name='Heating'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='kitchen',
            field=models.BooleanField(default=True, verbose_name='Kitchen'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='shower',
            field=models.BooleanField(default=True, verbose_name='Shower'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='size_of_balcony',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='size_of_bedrooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='size_of_kitchen',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='tv',
            field=models.BooleanField(default=True, verbose_name='TV'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='wifi',
            field=models.BooleanField(default=True, verbose_name='WIFI'),
        ),
    ]
