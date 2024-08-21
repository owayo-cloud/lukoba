from sqlalchemy import Boolean, Column, Date, Time, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_setup import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

    bookings = relationship('Booking', back_populates='user') #A one-to-many relationship with the Booking model. Each user can have multiple bookings


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    imdb = Column(String)
    description = Column(String)
    poster = Column(String)  # URL to the movie poster

    showtimes = relationship('Showtime', back_populates='movie')#A one-to-many relationship with the Showtime model. Each movie can have multiple showtimes


class Showtime(Base):
    __tablename__ = 'showtimes'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    time = Column(Time)
    seats_available = Column(Integer, default=25)

    movie_id = Column(Integer, ForeignKey('movies.id'))# A many-to-one relationship with the Movie model. Each showtime is associated with one movie.
    movie = relationship('Movie', back_populates='showtimes')# A one-to-many relationship with the Booking model. Each showtime can have multiple bookings
    bookings = relationship('Booking', back_populates='showtime') # A one-to-many relationship with the Seat model. Each showtime can have multiple seats
    seats = relationship('Seat', back_populates='showtime')


class Seat(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, ForeignKey('showtimes.id'))
    seat_number = Column(String)
    is_booked = Column(Boolean, default=True)

    showtime = relationship('Showtime', back_populates='seats')#A many-to-one relationship with the Showtime model. Each seat belongs to one showtime
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    booking = relationship('Booking', back_populates='seats')#A many-to-one relationship with the Booking model. Each seat can be associated with a booking


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='bookings')
    showtime_id = Column(Integer, ForeignKey('showtimes.id'))
    showtime = relationship('Showtime', back_populates='bookings')
    seats = relationship('Seat', back_populates='booking')
    payment_id = Column(Integer, ForeignKey('payments.id'))
    payment = relationship('Payment', back_populates='booking')


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    payment_method = Column(String)
    transaction_id = Column(String)

    booking = relationship('Booking', back_populates='payment')#A one-to-one relationship with the Booking model. Each payment is associated with one booking
