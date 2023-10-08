# Generated by Django 4.2.5 on 2023-10-05 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_rename_maximix_number_of_guests_apartment_maximum_number_of_guests'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyPricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.PositiveSmallIntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_prices', to='bookings.apartment')),
            ],
        ),
    ]
