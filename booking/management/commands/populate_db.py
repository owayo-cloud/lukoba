from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from booking.models import Movie, Showtime, Seat, Booking, Payment
from booking.utils import get_movie_data, search_movies
from faker import Faker
import random
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--movies', nargs='+', help='List of movie titles to add')
        parser.add_argument('--showtimes', type=int, default=20, help='Number of showtimes to create')
        parser.add_argument('--bookings', type=int, default=15, help='Number of bookings to create')

    def handle(self, *args, **options):
        num_users = options.get('users', 10)
        movie_titles = options.get('movies', [])
        num_showtimes = options.get('showtimes', 20)
        num_bookings = options.get('bookings', 15)

        if movie_titles:
            self.create_movies(movie_titles)
        
        self.create_users(num_users)
        self.create_showtimes(num_showtimes)
        self.create_bookings(num_bookings)
        self.create_payments()

    def create_users(self, num_users):
        """Create users"""
        fake = Faker()
        for _ in range(num_users):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            is_admin = fake.boolean(chance_of_getting_true=10)
            try:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_admin=is_admin
                )
            except Exception:
                pass  # Skip if user already exists
        self.stdout.write(self.style.SUCCESS(f'{num_users} users created.'))

    def create_movies(self, movie_titles):
        """Create movies using OMDB API"""
        for title in movie_titles:
            movie_data = get_movie_data(title)
            if movie_data and movie_data.get('Response') == 'True':
                Movie.objects.get_or_create(
                    imdb=movie_data.get('imdbID'),
                    defaults={
                        'title': movie_data.get('Title'),
                        'genre': movie_data.get('Genre', ''),
                        'description': movie_data.get('Plot', ''),
                        'poster': movie_data.get('Poster', '')
                    }
                )
            else:
                self.stdout.write(self.style.WARNING(f'Could not find data for movie: {title}'))
        self.stdout.write(self.style.SUCCESS(f'{len(movie_titles)} movies added.'))

    def create_showtimes(self, num_showtimes):
        """Create showtimes"""
        fake = Faker()
        movies = list(Movie.objects.all())
        if not movies:
            self.stdout.write(self.style.WARNING('No movies found. Please add movies first.'))
            return
        
        for _ in range(num_showtimes):
            movie = random.choice(movies)
            date = fake.date_between(start_date='-1y', end_date='+1y')
            time = fake.time_object()
            seats_available = random.randint(10, 25)
            Showtime.objects.create(
                movie=movie,
                date=date,
                time=time,
                seats_available=seats_available
            )
        self.stdout.write(self.style.SUCCESS(f'{num_showtimes} showtimes created.'))

    def create_bookings(self, num_bookings):
        """Create bookings and associated seats"""
        fake = Faker()
        users = list(User.objects.all())
        showtimes = list(Showtime.objects.all())
        
        if not users or not showtimes:
            self.stdout.write(self.style.WARNING('No users or showtimes found.'))
            return

        seat_rows = ['A', 'B', 'C', 'D', 'E']
        seat_numbers = [f"{row}{num}" for row in seat_rows for num in range(1, 6)]

        for _ in range(num_bookings):
            user = random.choice(users)
            showtime = random.choice(showtimes)

            # Determine how many seats to book for this booking (1-5 seats)
            num_seats_to_book = random.randint(1, 5)
            booked_seat_numbers = set(
                showtime.seats.filter(is_booked=True).values_list('seat_number', flat=True)
            )
            available_seat_numbers = list(set(seat_numbers) - booked_seat_numbers)

            if len(available_seat_numbers) >= num_seats_to_book:
                # Create payment first
                payment = Payment.objects.create(
                    amount=num_seats_to_book * 200,
                    payment_method='mpesa',
                    transaction_id=fake.uuid4()
                )

                # Create booking
                booking = Booking.objects.create(
                    user=user,
                    showtime=showtime,
                    payment=payment
                )

                # Create seats
                booked_seats = random.sample(available_seat_numbers, num_seats_to_book)
                for seat_number in booked_seats:
                    Seat.objects.create(
                        showtime=showtime,
                        seat_number=seat_number,
                        is_booked=True,
                        booking=booking
                    )

                # Update available seats
                showtime.seats_available -= num_seats_to_book
                showtime.save()

        self.stdout.write(self.style.SUCCESS(f'{num_bookings} bookings with seats created.'))

    def create_payments(self):
        """Create payments for bookings without payments"""
        bookings = Booking.objects.filter(payment__isnull=False)
        self.stdout.write(self.style.SUCCESS(f'Payments created for {bookings.count()} bookings.'))
