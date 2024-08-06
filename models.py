from sqlalchemy import Boolean, Column, DateTime, Date,Time,Float, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from db_setup import Base

booking_seats = Table('booking_seats', Base.metadata,
                      Column('booking_id', Integer, ForeignKey(
                          'bookings.id'), primary_key=True),
                      Column('seat_id', Integer, ForeignKey(
                          'seats.id'), primary_key=True)
                      )

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    bookings = relationship("Booking", backref="user")


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    imdb = Column(String)
    description = Column(String)
    poster = Column(String)  # URL to the movie poster
    bookings = relationship("Booking", backref="movie")
    showtimes = relationship("Showtime", backref="movie")

class Showtime(Base):
    __tablename__ = 'showtimes'

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    date = Column(Date)
    time = Column(Time)
    seats_available = Column(Integer,default=25)
    bookings = relationship("Booking", backref="showtime")
    seats = relationship("Seat", backref="showtime")
class Seat(Base):
    __tablename__ = 'seats'

    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, ForeignKey('showtimes.id'))
    seat_number = Column(String)
    is_booked = Column(Boolean, default=True)
    bookings = relationship(
        "Booking", secondary=booking_seats, back_populates="seats")
class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    showtime_id = Column(Integer, ForeignKey('showtimes.id'))
    payment_id = Column(Integer, ForeignKey(
        'payments.id'), nullable=True)  # Optional
    seats = relationship("Seat", secondary=booking_seats, back_populates="bookings")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    amount = Column(Float)
    payment_method = Column(String)
    transaction_id = Column(String)
