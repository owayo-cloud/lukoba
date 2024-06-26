from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
import random
import requests
from jinja2 import Environment, FileSystemLoader
from werkzeug.security import generate_password_hash, check_password_hash
from http import cookies
from db_setup import SessionLocal, init_db
from models import User, Movie, Booking
from urllib.parse import parse_qs

# Initialize the database
init_db()

OMDB_API_KEY = 'e89e6bd6'

env = Environment(loader=FileSystemLoader('templates'))

PREDEFINED_TITLES = ['Inception', 'The Dark Knight', 'Interstellar', 'The Matrix', 'Pulp Fiction', 'Fight Club', 'The Shawshank Redemption', 'The Godfather', 'The Avengers', 'The Social Network']


def get_movie_data(title):
    url = f'http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def search_movies(query):
    url = f'http://www.omdbapi.com/?s={query}&apikey={OMDB_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('Search', [])
    else:
        return []

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.handle_home()
        elif self.path == '/login':
            self.handle_login()
        elif self.path == '/register':
            self.handle_register()
        elif self.path == '/movies':
            self.handle_movies()
        elif self.path == '/dashboard':
            self.handle_dashboard()
        elif self.path == '/dashboard/movies':
            self.handle_dashboard_movies()
        elif self.path == '/booking':
            self.handle_book()
        elif self.path == '/logout':  # Add endpoint for logout
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
        elif self.path == '/book':
            self.handle_book_post()
        else:
            self.send_error(404, "File not found")

    def handle_home(self):
        template = env.get_template('index.html')
        session = self.get_session()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(template.render(session=session).encode())

    def handle_movies(self):
        template = env.get_template('movies.html')
        session = self.get_session()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(template.render(session=session).encode())

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
                title = PREDEFINED_TITLES[random.randint(0, 9)]
                movies = search_movies(title)
            template = env.get_template('dashboard_movies.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(template.render(session=session,movies=movies).encode())
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
        db = SessionLocal()
        movies = db.query(Movie).all()
        db.close()
        template = env.get_template('booking.html')
        session = self.get_session()
        if not session.get('user'):
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Pass session to the template
        self.wfile.write(template.render(
            movies=movies, session=session).encode())

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
        movie_id = form.getvalue('movie_id')
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
        if user is not None:
            new_booking = Booking(user_id=user.id, movie_id=movie_id)
        else:
            new_booking = Booking(movie_id=movie_id)
        db.add(new_booking)
        db.commit()
        db.close()
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

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


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    print(f'Open your browser and visit http://localhost:{port}/')
    httpd.serve_forever()


if __name__ == '__main__':
    run()

