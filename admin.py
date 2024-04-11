import mysql.connector
import hashlib
import json
import http.server
from urllib.parse import urlparse, parse_qs
from http import cookies

def register_admin(conn, cursor, username, email, password, profilePicture):
    hash_pass = hashlib.sha256(password.encode()).hexdigest() #hash password
    #insert user data to DB
    cursor.execute("INSERT INTO admin (username, email, password, profilePicture) VALUES (%s, %s, %s, %s)", (username, email, hash_pass, profilePicture))
    conn.commit()

def parse_cookies(cookie_str):
    parsed_cookies = cookies.SimpleCookie()
    parsed_cookies.load(cookie_str)
    return {key: parsed_cookies[key].value for key in parsed_cookies}

def login_admin(conn, cursor, email, password):
    hash_pass = hashlib.sha256(password.encode()).hexdigest() # Hash password
    # Check if admin with given email and password exists in DB
    cursor.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, hash_pass))
    user = cursor.fetchone()
    if user:
        #setting cookie upon successful login
        cookie = cookies.SimpleCookie()
        cookie['admin_email'] = email
        cookie['admin_email']['path'] = '/'
        cookie['admin_email']['httponly'] = True
        return {"status": "success", "message": "Login successful!", "cookie": cookie.output(header='')}
    else:
        return {"status": "error", "message": "Invalid email or password."}
    
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                username='root',
                password='1738',
                database='lukoba'
            )
            cursor = conn.cursor()
            
            # Read and parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # Parse request path and query parameters
            path = urlparse(self.path)
                
            if path.path.rstrip('/') == '/register':
                print('Received data:', data)
                register_admin(conn, cursor, data['username'], data['email'], data['password'], data['profilePicture'])
                response_data = {"status": "success", "message": "Registration successful!"}
            elif path.path.rstrip('/') == '/login':
                response_data = login_admin(conn, cursor, data['email'], data['password'])
            else:
                response_data = {"status": "error", "message": "Invalid endpoint"}

            # New route for admin login
            if path.path.rstrip('/') == '/admin_login':
                cookie_data = parse_cookies(self.headers.get('Cookie', ''))
                if 'admin_email' in cookie_data:
                    response_data = {"status": "success", "message": "Already logged in"}
                else:
                    response_data = login_admin(conn, cursor, data['email'], data['password'])
                    
                    # Redirect to dashboard after successful login
                    if response_data['status'] == 'success':
                        cookie = response_data['cookie']
                        self.send_header('Set-Cookie', cookie)
                        
                        # Finally, redirect to the dashboard upon successful login
                        self.send_response(302)
                        self.send_header('Location', '/dashboard')
                        self.end_headers()

        except mysql.connector.Error as e:
            response_data = {"status": "error", 'message': f'Error connecting to database: {e}'}

        finally:
            # Close the DB
            cursor.close()
            conn.close()

        # Sending http response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

def main():
    PORT = 8000
    with http.server.HTTPServer(("", PORT), RequestHandler) as httpd:
        print("server started on port", PORT)
        httpd.serve_forever()

if __name__ == "__main__":
    main()
