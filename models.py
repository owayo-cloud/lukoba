from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_setup import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    # imdb = Column(String)    
    description = Column(String)
    poster = Column(String)  # URL to the movie poster
    bookings = relationship("Booking", backref="movie")

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    
    
#A User can make many Bookings (one-to-many).
#A Movie can have many Bookings (one-to-many).
#A Booking is made by one User and is for one Movie (many-to-one).
#A Booking is associated with one Showtime (many-to-one).
#A Booking is associated with one Payment (many-to-one).
#A Payment is associated with one Booking (many-to-one).
