import argparse
import requests
from werkzeug.security import generate_password_hash
from faker import Faker
from db_setup import SessionLocal, init_db
from models import User, Movie, Showtime, Seat, Booking, Payment
import random
from datetime import datetime, timedelta

# Replace with your OMDb API key
OMDB_API_KEY = 'e89e6bd6'

# Initialize the database
init_db()

# Initialize Faker
fake = Faker()

# Function to fetch movie data from OMDb API


def get_movie_data(title):
    url = f'http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}'
    response = requests.get(url)
    print(f"Fetching data for {title}, Status code: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {title}")
        return None

# Function to search for movies using OMDb API


def search_movies(query):
    url = f'http://www.omdbapi.com/?s={query}&apikey={OMDB_API_KEY}&type=movie'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('Search', [])
    else:
        return []

# Function to create users


def create_users(num_users):
    db = SessionLocal()
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = generate_password_hash(fake.password())
        is_admin = fake.boolean(chance_of_getting_true=10)
        new_user = User(username=username, email=email,
                        password=password, is_admin=is_admin)
        db.add(new_user)
    db.commit()
    db.close()
    print(f"{num_users} users created.")

# Function to create movies using OMDb API


# Function to create movies using OMDb API
def create_movies(movie_titles):
    # Check if movie_titles is None or empty
    if not movie_titles:
        print("No movie titles provided.")
        return
    
    db = SessionLocal()
    for title in movie_titles:
        print(movie_titles)
        movie_data = get_movie_data(title)
        if movie_data and movie_data.get('Response') == 'True':
            new_movie = Movie(
                title=movie_data.get('Title'),
                genre=movie_data.get('Genre'),
                # Store imdbID instead of rating
                imdb=movie_data.get('imdbID'),
                description=movie_data.get('Plot'),
                poster=movie_data.get('Poster')
            )
            db.add(new_movie)
        else:
            print(f"Could not find data for movie: {title}")
    db.commit()
    db.close()
    print(f"{len(movie_titles)} movies added.")

# Function to create showtimes


def create_showtimes(num_showtimes):
    db = SessionLocal()
    movies = db.query(Movie).all()
    for _ in range(num_showtimes):
        movie = random.choice(movies)
        date = fake.date_between(start_date='-1y', end_date='+1y')
        time = fake.time_object()
        seats_available = random.randint(10, 25)
        new_showtime = Showtime(date=date, time=time,
                                seats_available=seats_available, movie_id=movie.id)
        db.add(new_showtime)
    db.commit()
    db.close()
    print(f"{num_showtimes} showtimes created.")


# Function to create bookings and associated seats
def create_bookings(num_bookings):
    db = SessionLocal()
    users = db.query(User).all()
    showtimes = db.query(Showtime).all()

    seat_rows = ['A', 'B', 'C', 'D', 'E']
    seat_numbers = [f"{row}{num}" for row in seat_rows for num in range(1, 6)]

    for _ in range(num_bookings):
        user = random.choice(users)
        showtime = random.choice(showtimes)

        # Determine how many seats to book for this booking (1-5 seats)
        num_seats_to_book = random.randint(1, 5)
        available_seat_numbers = list(
            set(seat_numbers) - set([seat.seat_number for seat in showtime.seats]))

        if len(available_seat_numbers) >= num_seats_to_book:
            new_booking = Booking(user_id=user.id, showtime_id=showtime.id)
            db.add(new_booking)
            db.commit()

            booked_seats = random.sample(
                available_seat_numbers, num_seats_to_book)
            for seat_number in booked_seats:
                new_seat = Seat(
                    showtime_id=showtime.id,
                    seat_number=seat_number,
                    is_booked=True,
                    booking_id=new_booking.id
                )
                db.add(new_seat)
                db.commit()

            #decrease the number of available seats by the number of booked seats
            showtime.seats_available -= num_seats_to_book # type: ignore
            db.commit()
        else:
            print(
                f"Not enough seats available for showtime {showtime.id}. Skipping booking.")

    db.close()
    print(f"{num_bookings} bookings with seats created.")

# Function to create payments


def create_payments():
    db = SessionLocal()
    bookings = db.query(Booking).all()
    for booking in bookings:
        # Calculate the total cost based on the number of seats booked
        num_seats = len(db.query(Seat).filter_by(booking_id=booking.id).all())
        amount = num_seats * 200  # Cost per seat is 200 shillings
        payment_method = random.choice(['Credit Card', 'PayPal', 'Cash'])
        transaction_id = fake.uuid4()
        new_payment = Payment(amount=amount, payment_method=payment_method,
                              transaction_id=transaction_id)

        booking.payment = new_payment
        db.add(new_payment)
        db.commit()
    db.close()
    print("Payments created for all bookings.")

# Main function


def main():
    parser = argparse.ArgumentParser(
        description="Populate the database with fake data")
    parser.add_argument('--users', type=int, default=10,
                        help="Number of users to create")
    parser.add_argument('--movies', nargs='+',
                        help="List of movie titles to add")
    parser.add_argument('--showtimes', type=int, default=20,
                        help="Number of showtimes to create")
    parser.add_argument('--bookings', type=int, default=15,
                        help="Number of bookings to create")

    args = parser.parse_args()

    create_users(args.users)
    create_movies(args.movies)
    create_showtimes(args.showtimes)
    create_bookings(args.bookings)
    create_payments()


if __name__ == "__main__":
    main()
