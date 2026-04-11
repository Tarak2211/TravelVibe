"""
Booking notification service — Email, WhatsApp (Twilio), SMS (Twilio)
"""
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _booking_context(booking):
    """Build a shared context dict from a Booking instance."""
    travelers = list(booking.travelers.all()) if hasattr(booking, 'travelers') else []
    return {
        'booking': booking,
        'travelers': travelers,
        'package': booking.package,
        'user': booking.user,
    }


# ─── EMAIL ────────────────────────────────────────────────────────────────────

def send_booking_email(booking):
    """Send booking confirmation email to the customer."""
    try:
        user = booking.user
        email = user.email
        if not email:
            logger.warning(f"No email for user {user.username}, skipping email.")
            return False

        subject = f"Booking Confirmed #{booking.booking_id} — {booking.package.title} | TravelVibe"

        ctx = _booking_context(booking)

        # Plain-text fallback
        message = (
            f"Hi {user.get_full_name() or user.username},\n\n"
            f"Your booking is CONFIRMED!\n\n"
            f"Booking ID   : {booking.booking_id}\n"
            f"Package      : {booking.package.title}\n"
            f"Destination  : {booking.package.destination.name}, {booking.package.destination.country}\n"
            f"Travel Date  : {booking.travel_date}\n"
            f"Travelers    : {booking.adults_count} Adult(s), {booking.children_count} Child(ren)\n"
            f"Total Amount : Rs.{booking.total_amount}\n"
            f"Amount Paid  : Rs.{booking.amount_paid}\n"
            f"Remaining    : Rs.{booking.remaining_amount}\n"
        )
        if booking.outbound_airline:
            message += (
                f"\nOutbound Flight: {booking.outbound_airline} {booking.outbound_flight_no}\n"
                f"  {booking.outbound_from} -> {booking.outbound_to}\n"
                f"  Departure: {booking.outbound_departure} | Arrival: {booking.outbound_arrival}\n"
            )
        if booking.return_airline:
            message += (
                f"\nReturn Flight: {booking.return_airline} {booking.return_flight_no}\n"
                f"  {booking.return_from} -> {booking.return_to}\n"
                f"  Departure: {booking.return_departure} | Arrival: {booking.return_arrival}\n"
            )
        message += f"\nThank you for booking with TravelVibe!\n— Team TravelVibe"

        # HTML template
        try:
            html_message = render_to_string('bookings/email/booking_confirmation.html', ctx)
        except Exception as tmpl_err:
            logger.warning(f"Email template error: {tmpl_err}")
            html_message = None

        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'TravelVibe <noreply@travelvibe.com>'

        # Only attempt SMTP if credentials are configured
        host_user = getattr(settings, 'EMAIL_HOST_USER', '')
        host_pass = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        if not host_user or not host_pass:
            logger.warning(f"Email not configured — skipping email for {booking.booking_id}")
            return False

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Booking email sent to {email} for {booking.booking_id}")
        return True

    except Exception as e:
        logger.error(f"Failed to send booking email for {booking.booking_id}: {e}")
        return False


# ─── TWILIO (SMS + WHATSAPP) ──────────────────────────────────────────────────

def _get_twilio_client():
    """Return a Twilio client if credentials are configured."""
    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    if not account_sid or not auth_token:
        return None
    try:
        from twilio.rest import Client
        return Client(account_sid, auth_token)
    except ImportError:
        logger.warning("twilio package not installed. Run: pip install twilio")
        return None


def _booking_sms_body(booking):
    user = booking.user
    name = user.get_full_name() or user.username
    return (
        f"Hi {name}! Your TravelVibe booking is CONFIRMED.\n"
        f"Booking ID: {booking.booking_id}\n"
        f"Package: {booking.package.title}\n"
        f"Destination: {booking.package.destination.name}\n"
        f"Travel Date: {booking.travel_date}\n"
        f"Amount: Rs.{booking.total_amount}\n"
        f"Have a great trip!"
    )


def send_booking_sms(booking):
    """Send booking confirmation SMS via Twilio."""
    try:
        phone = getattr(booking.user, 'phone_number', None)
        if not phone:
            logger.warning(f"No phone for user {booking.user.username}, skipping SMS.")
            return False

        client = _get_twilio_client()
        if not client:
            logger.warning("Twilio not configured, skipping SMS.")
            return False

        from_number = getattr(settings, 'TWILIO_PHONE_NUMBER', '')
        if not from_number:
            logger.warning("TWILIO_PHONE_NUMBER not set, skipping SMS.")
            return False

        msg = client.messages.create(
            body=_booking_sms_body(booking),
            from_=from_number,
            to=phone,
        )
        logger.info(f"SMS sent to {phone} for {booking.booking_id}, SID: {msg.sid}")
        return True

    except Exception as e:
        logger.error(f"Failed to send SMS for {booking.booking_id}: {e}")
        return False


def send_booking_whatsapp(booking):
    """Send booking confirmation via WhatsApp (Twilio WhatsApp sandbox)."""
    try:
        phone = getattr(booking.user, 'phone_number', None)
        if not phone:
            logger.warning(f"No phone for user {booking.user.username}, skipping WhatsApp.")
            return False

        client = _get_twilio_client()
        if not client:
            logger.warning("Twilio not configured, skipping WhatsApp.")
            return False

        whatsapp_from = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

        # Ensure phone is in whatsapp: format
        to_number = phone if phone.startswith('whatsapp:') else f'whatsapp:{phone}'

        msg = client.messages.create(
            body=_booking_sms_body(booking),
            from_=whatsapp_from,
            to=to_number,
        )
        logger.info(f"WhatsApp sent to {phone} for {booking.booking_id}, SID: {msg.sid}")
        return True

    except Exception as e:
        logger.error(f"Failed to send WhatsApp for {booking.booking_id}: {e}")
        return False


# ─── COMBINED SENDER ──────────────────────────────────────────────────────────

def send_all_booking_notifications(booking):
    """Send Email + SMS + WhatsApp for a booking. Failures are logged, not raised."""
    results = {
        'email': send_booking_email(booking),
        'sms': send_booking_sms(booking),
        'whatsapp': send_booking_whatsapp(booking),
    }
    logger.info(f"Notification results for {booking.booking_id}: {results}")
    return results
