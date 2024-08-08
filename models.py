from sqlalchemy import Boolean, Column, DateTime, Date, Time, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_setup import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

    bookings = relationship('Booking', back_populates='user')


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    imdb = Column(String)
    description = Column(String)
    poster = Column(String)  # URL to the movie poster

    showtimes = relationship('Showtime', back_populates='movie')


class Showtime(Base):
    __tablename__ = 'showtimes'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    time = Column(Time)
    seats_available = Column(Integer, default=25)

    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship('Movie', back_populates='showtimes')
    bookings = relationship('Booking', back_populates='showtime')
    seats = relationship('Seat', back_populates='showtime')


class Seat(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, ForeignKey('showtimes.id'))
    seat_number = Column(String)
    is_booked = Column(Boolean, default=True)

    showtime = relationship('Showtime', back_populates='seats')
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    booking = relationship('Booking', back_populates='seats')


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

    booking = relationship('Booking', back_populates='payment')
