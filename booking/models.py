from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom User model with admin flag"""
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'


class Movie(models.Model):
    """Movie model"""
    title = models.CharField(max_length=255, db_index=True)
    genre = models.CharField(max_length=255)
    imdb = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    poster = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movies'
        ordering = ['title']


class Showtime(models.Model):
    """Showtime model"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    date = models.DateField()
    time = models.TimeField()
    seats_available = models.IntegerField(default=25)

    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time}"

    class Meta:
        db_table = 'showtimes'
        ordering = ['date', 'time']


class Seat(models.Model):
    """Seat model"""
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=True)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='seats', null=True, blank=True)

    def __str__(self):
        return f"{self.showtime} - Seat {self.seat_number}"

    class Meta:
        db_table = 'seats'
        unique_together = ['showtime', 'seat_number']


class Payment(models.Model):
    """Payment model"""
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.amount}"

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']


class Booking(models.Model):
    """Booking model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='booking')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.showtime.movie.title}"

    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
