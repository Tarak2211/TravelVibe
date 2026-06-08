from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking


@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance, created, **kwargs):
    """
    Fire notifications only when status changes to 'confirmed' on an existing booking.
    New bookings are handled explicitly in the view (after travelers are saved),
    so we skip created=True here to avoid double-sending and empty traveler lists.
    """
    if not created and instance.status == 'confirmed':
        try:
            from .notifications import send_all_booking_notifications
            send_all_booking_notifications(instance)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Notification error: {e}")
