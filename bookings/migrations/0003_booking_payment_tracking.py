from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_add_flight_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(
                max_length=20,
                choices=[('unpaid','Unpaid'),('partial','Partial Payment'),('paid','Fully Paid'),('refunded','Refunded')],
                default='unpaid',
            ),
        ),
        migrations.AddField(
            model_name='booking',
            name='amount_paid',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                      help_text='Amount paid so far'),
        ),
        migrations.AddField(
            model_name='booking',
            name='remaining_amount',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                      help_text='Balance due'),
        ),
        migrations.AddField(
            model_name='booking',
            name='remaining_due_date',
            field=models.DateField(null=True, blank=True,
                                   help_text='Date by which remaining payment must be made'),
        ),
        migrations.AddField(
            model_name='booking',
            name='payment_notes',
            field=models.TextField(blank=True, default='',
                                   help_text='Any notes about payment arrangement'),
        ),
    ]
