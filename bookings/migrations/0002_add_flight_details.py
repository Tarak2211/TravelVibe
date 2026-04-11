# Generated migration to add flight details to Booking model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='outbound_airline',
            field=models.CharField(max_length=100, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='outbound_flight_no',
            field=models.CharField(max_length=20, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='outbound_departure',
            field=models.CharField(max_length=20, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='outbound_arrival',
            field=models.CharField(max_length=20, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='outbound_duration',
            field=models.CharField(max_length=20, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='outbound_stops',
            field=models.CharField(max_length=100, blank=True, default='Direct'),
        ),
        migrations.AddField(
            model_name='booking',
            name='outbound_from',
            field=models.CharField(max_length=50, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='outbound_to',
            field=models.CharField(max_length=50, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='return_airline',
            field=models.CharField(max_length=100, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='return_flight_no',
            field=models.CharField(max_length=20, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='return_departure',
            field=models.CharField(max_length=20, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='return_arrival',
            field=models.CharField(max_length=20, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='return_duration',
            field=models.CharField(max_length=20, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='return_stops',
            field=models.CharField(max_length=100, blank=True, default='Direct'),
        ),
        migrations.AddField(
            model_name='booking',
            name='return_from',
            field=models.CharField(max_length=50, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='return_to',
            field=models.CharField(max_length=50, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='seat_class',
            field=models.CharField(max_length=20, blank=True, default='Economy'),
        ),
    ]
