import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
import os
import random
import subprocess
import requests
from requests.auth import HTTPBasicAuth
from jinja2 import Environment, FileSystemLoader
from werkzeug.security import generate_password_hash, check_password_hash
from http import cookies
from db_setup import SessionLocal, init_db
from models import Seat, Showtime, User, Movie, Booking,Payment
from urllib.parse import parse_qs
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import sys
from datetime import datetime, time
from sqlalchemy.orm import joinedload

# Initialize the database
init_db()


OMDB_API_KEY = 'e89e6bd6'

env = Environment(loader=FileSystemLoader('templates'))

PREDEFINED_TITLES = ['Inception', 'The Dark Knight', 'Interstellar', 'The Matrix', 'Pulp Fiction',
                     'Fight Club', 'The Shawshank Redemption', 'The Godfather', 'The Avengers', 'The Social Network']
def run_migrations():
    subprocess.run(["alembic", "upgrade", "head"])

def generate_access_token(consumer_key, consumer_secret):
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = response.json()['access_token']
    return access_token

def lipa_na_mpesa_online(access_token, business_short_code, lipa_na_mpesa_online_passkey, amount, phone_number, callback_url, account_reference, transaction_desc):
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': 'Bearer %s' % access_token}
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = business_short_code + lipa_na_mpesa_online_passkey + timestamp
    online_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

    payload = {
        "BusinessShortCode": "174379",    
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",    
        "Timestamp":"20160216165627",    
        "TransactionType": "CustomerPayBillOnline",    
        "Amount": f"{amount}",    
        "PartyA":"254717702346",    
        "PartyB":"174379",    
        "PhoneNumber":f'{phone_number}',    
        "CallBackURL": callback_url,    
        "AccountReference":"Test",    
        "TransactionDesc":"Test"
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def get_movie_data(title):
    url = f'http://www.omdbapi.com/?i={title}&apikey={OMDB_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def search_movies(query):
    url = f'http://www.omdbapi.com/?s={query}&apikey={OMDB_API_KEY}&type=movie'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('Search', [])
    else:
        return []


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.handle_home()
        elif self.path == '/contacts':
            self.handle_contacts()
        elif self.path == '/movies':
            self.handle_movies()
        elif self.path.startswith('/movies?title='):
            self.handle_movies()
        elif self.path.startswith('/movies/tt') and (self.path.split('/')[-1] == 'book' or self.path.split('/')[-1].split('?')[0] == 'book' ):
            self.handle_book()
        elif self.path.startswith('/movies/tt') and self.path.split('/')[-1] == 'payment':
            self.handle_payment_status()
        elif self.path.startswith('/movies/tt'):
            self.handle_movie_detail()
        elif self.path == '/login':
            self.handle_login()
        elif self.path == '/register':
            self.handle_register()
        elif self.path == '/dashboard':
            self.handle_dashboard()
        elif self.path == '/dashboard/movies':
            self.handle_dashboard_movies()
        elif self.path == '/dashboard/analytics':
            self.handle_dashboard_analytics()
        elif self.path == '/dashboard/bookings':
            self.handle_dashboard_bookings()
        elif self.path == '/dashboard/users':
            self.handle_dashboard_users()
        elif self.path.startswith('/dashboard/movies?title='):
            self.handle_dashboard_movies()
        elif self.path.startswith('/dashboard/movies/tt'):
            self.handle_dashboard_movie_detail()
        elif self.path == '/booking':
            self.handle_book()
        elif self.path == '/logout':
            self.handle_logout()
        elif self.path.startswith('/static/'):  # Handle static file requests
            static_path = os.path.join('static', self.path[len('/static/'):])
            if os.path.isfile(static_path):
                with open(static_path, 'rb') as f:
                    file_content = f.read()
                    content_type = 'text/css' if static_path.endswith(
                        '.css') else 'application/octet-stream'
                    self.send_response(200)
                    self.send_header('Content-type', content_type)
                    self.end_headers()
                    self.wfile.write(file_content)
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == '/login':
            self.handle_login_post()
        elif self.path == '/register':
            self.handle_register_post()
        elif self.path.startswith('/movies/tt') and self.path.split('/')[-1] == 'book':
            self.handle_book_post()
        elif self.path == '/dashboard/movies/add':
            self.handle_add_movie_post()
        elif self.path.startswith('/dashboard/movies/delete/'):
            showtime_id = int(self.path.split('/')[-1])
            self.handle_delete_showtime(showtime_id)
        elif self.path == '/mpesa_callback':
            self.handle_mpesa_callback_post()
        else:
            self.send_error(404, "File not found")
            

    def handle_add_movie_post(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
                                'REQUEST_METHOD': 'POST'})
        movie_id = form.getvalue('movie')
        date = form.getvalue('date')
        time_str = form.getvalue('time')

        db = SessionLocal()
        # get movie with id
        movie = db.query(Movie).filter(Movie.imdb == movie_id).first()
        # if not found create
        if not movie:
            data = get_movie_data(movie_id)
            if data:
                title = data.get('Title')
                genre = data.get('Genre')
                description = data.get('Plot')
                poster = data.get('Poster')
                movie = Movie(title=title, genre=genre,
                              description=description, poster=poster, imdb=movie_id)
                db.add(movie)
                db.commit()
            else:
                self.send_error(404, "Movie not found")
                return

        # Parse the date string
        date_obj = datetime.strptime(date, '%Y-%m-%d')

        # Extract the time portion as a time object
        time_obj = time.fromisoformat(time_str)
        showtime = Showtime(movie_id=movie.id, date=date_obj, time=time_obj)

        db.add(showtime)
        db.commit()
        db.close()

        self.send_response(302)
        self.send_header('Location', f'/dashboard/movies/{movie_id}')
        self.end_headers()

    def handle_delete_showtime(self, showtime_id):
        db = SessionLocal()
        showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
        if showtime:
            db.delete(showtime)
            db.commit()
            db.close()
            self.send_response(302)
            self.send_header('Location', f'/dashboard/movies/{showtime.movie_id}?showtime_deleted=true')
            self.end_headers()
        else:
            db.close()
            self.send_error(404, "Showtime not found")

    def handle_home(self):
        db = SessionLocal()
        movies = db.query(Movie).all()
        db.close()

        template = env.get_template('home.html')
        session = self.get_session()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(template.render(
            session=session, movies=movies).encode())
        
    def handle_contacts(self):
        template = env.get_template('contacts.html')
        session = self.get_session()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(template.render(session=session).encode())

    def handle_movies(self):
        session = self.get_session()
        query = self.path.split('?')[-1]
        query_params = parse_qs(query)
        title = query_params.get('title', [None])[0]
        print(title, query_params)
        movies = []
        if title:
            movies = search_movies(title)
        else:
            # get random query from predefined_list and pass it as title
            title = random.choice(PREDEFINED_TITLES)
            movies = search_movies(title)
        template = env.get_template('movies.html')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(template.render(
            session=session, movies=movies).encode())

    def handle_dashboard(self):
        session = self.get_session()
        if session.get('is_admin') == 'true':
            template = env.get_template('dashboard.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(template.render(session=session).encode())
        else:
            self.send_error(403, "Forbidden")

    def handle_dashboard_movies(self):
        session = self.get_session()
        if session.get('is_admin') == 'true':
            query = self.path.split('?')[-1]
            query_params = parse_qs(query)
            title = query_params.get('title', [None])[0]
            movies = []
            if title:
                movies = search_movies(title)
            else:
                # get random query from predefined_list and pass it as title
                title = random.choice(PREDEFINED_TITLES)
                movies = search_movies(title)
            template = env.get_template('dashboard_movies.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(template.render(
                session=session, movies=movies).encode())
        else:
            self.send_error(403, "Forbidden")

    def handle_dashboard_movie_detail(self):
        session = self.get_session()
        if session.get('is_admin') == 'true':
            title = self.path.split('/')[-1]
            if title:
                movie = get_movie_data(title)
                # get showtimes
                db = SessionLocal()
                movie_obj = db.query(Movie).filter_by(imdb=title).first()
                if movie_obj:
                    showtimes = movie_obj.showtimes
                else:
                    showtimes = None
                db.close()

                template = env.get_template('dashboard_movie_detail.html')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(template.render(
                    session=session, movie=movie, showtimes=showtimes).encode())
            else:
                self.send_error(404, "Movie not found")
        else:
            self.send_error(403, "Forbidden")

    def handle_movie_detail(self):
        session = self.get_session()
        
        title = self.path.split('/')[-1]
        if title:
            movie = get_movie_data(title)
            # get showtimes
            db = SessionLocal()
            movie_obj = db.query(Movie).filter_by(imdb=title).first()
            if movie_obj:
                showtimes = movie_obj.showtimes
            else:
                showtimes = None
            db.close()

            template = env.get_template('movie_detail.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(template.render(
                session=session, movie=movie, showtimes=showtimes).encode())
        else:
            self.send_error(404, "Movie not found")

    def handle_payment_status(self):
        session = self.get_session()
        
        booking = self.path.split('/')[-2]
        booking_obj = None
        user = None
        db = SessionLocal()

        if booking:
            db = SessionLocal()
            booking_obj = db.query(Booking).filter_by(id=booking).first()
            if booking_obj:
                user = db.query(User).filter_by(id=booking_obj.user_id).first()
            db.close()

        template = env.get_template('payment.html')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(template.render(
                session=session, booking=booking_obj,user=user).encode())

    def handle_dashboard_analytics(self):
        session = self.get_session()
        if session.get('is_admin') == 'true':
            template = env.get_template('dashboard_analytics.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(template.render(session=session).encode())
        else:
            self.send_error(403, "Forbidden")


    def handle_dashboard_bookings(self):
        db = SessionLocal()
        try:
            bookings = db.query(Booking).options(
                joinedload(Booking.user),
                joinedload(Booking.showtime),
                joinedload(Booking.payment)
            ).all()
            
            session = self.get_session()
            if session.get('is_admin') == 'true':
                template = env.get_template('dashboard_bookings.html')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(template.render(session=session, bookings=bookings).encode())
            else:
                self.send_error(403, "Forbidden")
        finally:
            db.close()


    def handle_dashboard_users(self):
        session = self.get_session()
        if session.get('is_admin') == 'true':
            template = env.get_template('dashboard_users.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(template.render(session=session).encode())
        else:
            self.send_error(403, "Forbidden")

    def handle_login(self):
        template = env.get_template('login.html')
        session = self.get_session()  # Retrieve session
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Pass session to the template
        self.wfile.write(template.render(session=session).encode())

    def handle_register(self):
        template = env.get_template('register.html')
        session = self.get_session()  # Retrieve session
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Pass session to the template
        self.wfile.write(template.render(session=session).encode())

    def handle_book(self):
        title = self.path.split('/')[-2]
        session = self.get_session() 
        query = self.path.split('?')[-1]
        query_params = parse_qs(query)
        showtime = query_params.get('s', [None])[0] #extracts the value of the s parameter If s is not present, showtime will be None.
        booked_seats = []
        if not session.get('user'):
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            return

        if title:
            # get showtimes
            db = SessionLocal()
            movie = db.query(Movie).filter_by(imdb=title).first()
            if movie:
                showtimes = movie.showtimes
                # get booked seats
            else:
                showtimes = None
            db.close()

            showtime_obj = db.query(Showtime).filter_by(id=showtime).first()
            if showtime_obj:
                # get booked seats
                booked_seats = [seat.seat_number for seat in showtime_obj.seats]

            template = env.get_template('booking.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(template.render(
                session=session, movie=movie, bookings=booked_seats, s_time=showtime_obj, showtimes=showtimes).encode())
        else:
            self.send_error(404, "Movie not found")

    def handle_login_post(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
            'REQUEST_METHOD': 'POST'})
        email = form.getvalue('email')
        password = form.getvalue('password')
        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        db.close()

        if user and check_password_hash(user.password, password):  # type: ignore
            self.send_response(302)
            self.send_header('Location', '/')
            self.send_header('Set-Cookie', f'user={user.username}')
            if user.is_admin:  # type: ignore
                self.send_header('Set-Cookie', 'is_admin=true')
            self.end_headers()
        else:
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()

    def handle_register_post(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
            'REQUEST_METHOD': 'POST'})
        username = form.getvalue('username')
        email = form.getvalue('email')
        password = form.getvalue('password')
        hashed_password = generate_password_hash(password)
        db = SessionLocal()
        new_user = User(username=username, email=email,
                        password=hashed_password)
        db.add(new_user)
        db.commit()
        db.close()
        self.send_response(302)
        self.send_header('Location', '/login')
        self.end_headers()

    def handle_book_post(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
            'REQUEST_METHOD': 'POST'})
        imdb = form.getvalue('imdb')
        movie = form.getvalue('movie')
        seats = form.getvalue('seats')
        showtime = form.getvalue('showtime')
        phone_number = form.getvalue('phone_number')  # Collect phone number for payment
        amount = form.getvalue('amount')  # Collect the amount for payment

        session = self.get_session()
        if not session.get('user'):
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            return

        db = SessionLocal()
        if session is not None:
            user = db.query(User).filter(
                User.username == session['user']).first()
        else:
            user = None

        user = db.query(User).filter(User.username == session['user']).first()
        if user is not None:
            try:
                movie = int(movie) # Retrieve the movie name using the movie_id
            except ValueError:

                if movie is not None:
                    db.close()
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("Error.".encode('utf-8'))
                    return
            
            # Retrieve the movie title using the movie_id
            movie = db.query(Movie).filter(Movie.id == movie).first()
            if not movie:
                db.close()
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Movie not found.".encode('utf-8'))
                return
        
            movie_title = movie.title
            print('movie title:', movie_title)

            show_obj = db.query(Showtime).filter(Showtime.id == showtime).first()
            if not show_obj:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Showtime not found.".encode('utf-8'))
                return
            
            #check if seats are available
            booked_seats = db.query(Seat).filter(Seat.showtime_id == showtime, Seat.is_booked == True).all()
            booked_seat_numbers = {seat.seat_number for seat in booked_seats}
            selected_seats = seats.split(',')
            print(f"Selected Seats Count: {selected_seats}")

            if any(seat in booked_seat_numbers for seat in selected_seats):
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Some selected seats are already booked.".encode('utf-8'))
                return
            
            # M-Pesa integration
            consumer_key = '3VfCkaY5Lxs9jZqCGn2lpRKdFeXladKgr08sQ41sHWUY0ppO'
            consumer_secret = 'G9jR9ZWyb5XlXP8HmgbSgMmpXsmR8RkqfqSxD9Tzn5Ei6cScAXLhShryVDUP7pO1'
            business_short_code = '174379'
            lipa_na_mpesa_online_passkey = 'MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3'
            callback_url = "https://1c67-41-72-192-194.ngrok-free.app///mpesa_callback"
            account_reference = 'LuKoBa'
            transaction_desc = 'Payment for booking'

            access_token = generate_access_token(consumer_key, consumer_secret)
            payment_response = lipa_na_mpesa_online(
                access_token,
                business_short_code,
                lipa_na_mpesa_online_passkey,
                amount,
                phone_number,
                callback_url,
                account_reference,
                transaction_desc
            )
            print("Payment Response:", payment_response)
            # Check if payment was successful
            if payment_response['ResponseCode'] == '0':
                # create payment
                payment = Payment(payment_method='mpesa', amount=amount, transaction_id=phone_number)
                db.add(payment)
                db.flush()

                new_booking = Booking(
                    user_id=user.id, showtime_id=showtime,payment_id=payment.id)

                db.add(new_booking)
                db.flush()  # This assigns an id to new_booking

                # Create and associate seats
                for seat_number in selected_seats:
                    # Create new seat
                    seat = Seat(
                        showtime_id=showtime,
                        seat_number=seat_number,
                        is_booked = True
                    )
                    db.add(seat)

                    new_booking.seats.append(seat)

                # Update available seats in showtime obj
                show_obj = db.query(Showtime).filter(
                    Showtime.id == showtime).first()

                if show_obj is not None:
                    seats_to_decrease = len(selected_seats)
                    show_obj.seats_available -= seats_to_decrease  # type: ignore
                    print(f"Updated Seats Available: {show_obj.seats_available}")
                # Commit the transaction
                db.commit()
                self.send_response(302)
                self.send_header('Location', f'/movies/{imdb}/{new_booking.id}/payment')
                self.end_headers()
            else:
                # Handle failed payment
                self.send_response(302)
                self.send_header('Location', f'/movies/{imdb}/payment_failed')
                self.end_headers()

            db.close()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(payment_response).encode('utf-8'))

        else:
            db.close()
            self.send_response(400)
            self.send_header('Location', f'/movies/{imdb}')
            self.end_headers()

    def handle_mpesa_callback_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        callback_data = json.loads(post_data)

        # Process the callback data
        print("M-pesa Callback Data:", callback_data)

        payment_status = callback_data.get('Body',{}).get('stkCallback', {}).get('ResultCode')

        if payment_status == 0: #0 indicates success in m-pesa transactions
            # payment was successful
            print("Payment successful. Proceed.")

        response = {'ResultCode': 0, 'ResultDesc': 'Accepted'}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def handle_logout(self):  # Add this method
        self.send_response(302)
        self.send_header('Location', '/')
        self.send_header('Set-Cookie', 'user=')
        self.send_header('Set-Cookie', 'is_admin=')
        self.end_headers()

    def get_session(self):
        session = {}
        if 'Cookie' in self.headers:
            cookie = cookies.SimpleCookie(self.headers['Cookie'])
            if 'user' in cookie:
                session['user'] = cookie['user'].value
            if 'is_admin' in cookie:
                session['is_admin'] = cookie['is_admin'].value
        return session


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, restart_function):
        super().__init__()
        self.restart_function = restart_function

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'{event.src_path} has been modified, restarting server...')
            self.restart_function()


def restart_server():
    print('Restarting server...')
    python = sys.executable
    os.execl(python, python, *sys.argv)


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    print(f'Open your browser and visit http://localhost:{port}/')

    observer = Observer()
    event_handler = ChangeHandler(restart_server)
    observer.schedule(event_handler, path='.', recursive=True)
    observer_thread = threading.Thread(target=observer.start)
    observer_thread.daemon = True
    observer_thread.start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    observer.stop()
    observer_thread.join()


if __name__ == '__main__':
    run()
