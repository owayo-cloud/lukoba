from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Movie, Showtime, Seat, Booking, Payment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    list_display = ['username', 'email', 'is_admin', 'is_staff', 'is_active']
    list_filter = ['is_admin', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_admin',)}),
    )


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Movie Admin"""
    list_display = ['title', 'genre', 'imdb']
    search_fields = ['title', 'genre']
    list_filter = ['genre']


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    """Showtime Admin"""
    list_display = ['movie', 'date', 'time', 'seats_available']
    list_filter = ['date', 'movie']
    search_fields = ['movie__title']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    """Seat Admin"""
    list_display = ['showtime', 'seat_number', 'is_booked', 'booking']
    list_filter = ['is_booked', 'showtime']
    search_fields = ['seat_number', 'showtime__movie__title']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Booking Admin"""
    list_display = ['id', 'user', 'showtime', 'payment', 'created_at']
    list_filter = ['created_at', 'showtime__movie']
    search_fields = ['user__username', 'showtime__movie__title']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Payment Admin"""
    list_display = ['id', 'amount', 'payment_method', 'transaction_id', 'created_at']
    list_filter = ['payment_method', 'created_at']
    search_fields = ['transaction_id']
