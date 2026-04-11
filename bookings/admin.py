from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Booking, Traveler, Payment, Coupon, SavedTraveler, Inquiry


class TravelerInline(admin.TabularInline):
    model = Traveler
    extra = 1
    fields = ['name', 'age', 'gender']


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ['transaction_id', 'payment_method', 'payment_type', 'amount', 'status', 'payment_date']
    readonly_fields = ['payment_date']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_id', 'user', 'package_name', 'duration_display',
        'travel_date', 'total_amount_display', 'amount_paid_display',
        'remaining_display', 'payment_status_badge', 'status_badge', 'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at', 'travel_date']
    search_fields = ['booking_id', 'user__username', 'user__email', 'package__title']
    readonly_fields = ['booking_id', 'remaining_amount', 'payment_status', 'created_at', 'updated_at', 'booking_summary']
    inlines = [TravelerInline, PaymentInline]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Booking Info', {
            'fields': ('booking_id', 'user', 'package', 'travel_date', 'status', 'created_at', 'updated_at')
        }),
        ('Travelers', {
            'fields': ('adults_count', 'children_count'),
        }),
        ('Payment Details', {
            'fields': (
                'base_fare', 'tax_amount', 'discount_amount', 'coupon',
                'total_amount', 'amount_paid', 'remaining_amount',
                'payment_status', 'remaining_due_date', 'payment_notes',
            ),
            'classes': ('wide',),
        }),
        ('Flight Details — Outbound', {
            'fields': (
                'outbound_airline', 'outbound_flight_no', 'outbound_from', 'outbound_to',
                'outbound_departure', 'outbound_arrival', 'outbound_duration', 'outbound_stops', 'seat_class',
            ),
            'classes': ('collapse',),
        }),
        ('Flight Details — Return', {
            'fields': (
                'return_airline', 'return_flight_no', 'return_from', 'return_to',
                'return_departure', 'return_arrival', 'return_duration', 'return_stops',
            ),
            'classes': ('collapse',),
        }),
        ('Summary', {
            'fields': ('booking_summary',),
        }),
    )

    # ── Custom display columns ──────────────────────────────────────────────

    def package_name(self, obj):
        return obj.package.title
    package_name.short_description = 'Package'

    def duration_display(self, obj):
        return obj.package.get_duration_display()
    duration_display.short_description = 'Duration'

    def total_amount_display(self, obj):
        return format_html('<strong>₹{}</strong>', obj.total_amount)
    total_amount_display.short_description = 'Total'

    def amount_paid_display(self, obj):
        color = '#10b981' if obj.amount_paid >= obj.total_amount else '#f59e0b'
        return format_html('<span style="color:{}; font-weight:700;">₹{}</span>', color, obj.amount_paid)
    amount_paid_display.short_description = 'Paid'

    def remaining_display(self, obj):
        if obj.remaining_amount <= 0:
            return format_html('<span style="color:#10b981; font-weight:700;">✓ Cleared</span>')
        color = '#ef4444'
        due = f" (due {obj.remaining_due_date})" if obj.remaining_due_date else ''
        return format_html('<span style="color:{}; font-weight:700;">₹{}{}</span>', color, obj.remaining_amount, due)
    remaining_display.short_description = 'Remaining'

    def payment_status_badge(self, obj):
        colors = {
            'unpaid': ('#ef4444', 'Unpaid'),
            'partial': ('#f59e0b', 'Partial'),
            'paid': ('#10b981', 'Paid'),
            'refunded': ('#6366f1', 'Refunded'),
        }
        color, label = colors.get(obj.payment_status, ('#64748b', obj.payment_status))
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;">{}</span>',
            color, label
        )
    payment_status_badge.short_description = 'Payment'

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'confirmed': '#10b981',
            'cancelled': '#ef4444',
            'completed': '#6366f1',
        }
        color = colors.get(obj.status, '#64748b')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def booking_summary(self, obj):
        travelers = obj.travelers.all()
        traveler_list = ', '.join([f"{t.name} ({t.age})" for t in travelers]) or '—'
        due_info = f"Due by {obj.remaining_due_date}" if obj.remaining_due_date else 'No due date set'
        return format_html('''
            <div style="background:#f0f9ff;border-radius:10px;padding:16px;font-family:sans-serif;font-size:13px;line-height:2;">
                <div><b>📦 Package:</b> {package} &nbsp;|&nbsp; <b>⏱ Duration:</b> {duration}</div>
                <div><b>📅 Travel Date:</b> {travel_date} &nbsp;|&nbsp; <b>👥 Travelers:</b> {adults} adult(s), {children} child(ren)</div>
                <div><b>💰 Total:</b> ₹{total} &nbsp;|&nbsp; <b>✅ Paid:</b> ₹{paid} &nbsp;|&nbsp; <b>⏳ Remaining:</b> ₹{remaining}</div>
                <div><b>📆 Remaining Due:</b> {due_info}</div>
                <div><b>🧳 Traveler Names:</b> {travelers}</div>
                {notes}
            </div>
        ''',
            package=obj.package.title,
            duration=obj.package.get_duration_display(),
            travel_date=obj.travel_date,
            adults=obj.adults_count,
            children=obj.children_count,
            total=obj.total_amount,
            paid=obj.amount_paid,
            remaining=obj.remaining_amount,
            due_info=due_info,
            travelers=traveler_list,
            notes=format_html('<div><b>📝 Notes:</b> {}</div>', obj.payment_notes) if obj.payment_notes else '',
        )
    booking_summary.short_description = 'Booking Summary'


@admin.register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'booking']
    list_filter = ['gender']
    search_fields = ['name', 'booking__booking_id']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'booking', 'amount', 'payment_method', 'status', 'payment_date']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['transaction_id', 'booking__booking_id']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'valid_from', 'valid_to', 'is_active', 'used_count', 'usage_limit']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']


@admin.register(SavedTraveler)
class SavedTravelerAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'user', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['name', 'user__username']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'package', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
