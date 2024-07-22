from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Float, Time
from sqlalchemy.orm import relationship
from db_setup import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

    bookings = relationship("Booking", back_populates="user")

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    genre = Column(String)
    description = Column(String)
    release_date = Column(DateTime)

    bookings = relationship("Booking", back_populates="movie")
    showtimes = relationship("Showtime", back_populates="movie")

class Showtime(Base):
    __tablename__ = 'showtimes'

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    show_date = Column(DateTime)
    show_time = Column(Time)

    movie = relationship("Movie", back_populates="showtimes")
    bookings = relationship("Booking", back_populates="showtime")

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    payment_id = Column(Integer, ForeignKey('payments.id'))
    showtime_id = Column(Integer, ForeignKey('showtimes.id'))

    user = relationship("User", back_populates="bookings")
    movie = relationship("Movie", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking")
    showtime = relationship("Showtime", back_populates="bookings")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    payment_date = Column(DateTime)
    booking_id = Column(Integer, ForeignKey('bookings.id'))

    booking = relationship("Booking", back_populates="payment")
    
    
#A User can make many Bookings (one-to-many).
#A Movie can have many Bookings (one-to-many).
#A Booking is made by one User and is for one Movie (many-to-one).
#A Booking is associated with one Showtime (many-to-one).
#A Booking is associated with one Payment (many-to-one).
#A Payment is associated with one Booking (many-to-one).
#A Showtime is associated with one Movie (many-to-one).
#A Movie can have many Showtimes (one-to-many).
#A Showtime can have many Bookings (one-to-many).
#A Booking is associated with one Showtime (many-to-one).