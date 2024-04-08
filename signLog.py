import mysql.connector
import http.server
import json
import hashlib
from urllib.parse import urlparse, parse_qs

def register_user(conn, cursor, username, email, password):
    hash_pass = hashlib.sha256(password.encode()).hexdigest() #hash password
    #insert user data to DB
    cursor.execute("INSERT INTO users (username, email, password) VALUES(%s, %s, %s)", (username, email, hash_pass))
    conn.commit()

def login_user(conn, cursor, email, password):
    hash_pass = hashlib.sha256(password.encode()).hexdigest() # Hash password
    # Check if user with given email and password exists in DB
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hash_pass))
    user = cursor.fetchone()
    if user:
        return {"status": "success", "message": "Login successful!"}
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
                host = 'localhost',
                username = 'root',
                password = '1738',
                database = 'lukoba'
            )
            cursor = conn.cursor()
            
            #read and parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            #parse request path and query parameters
            path = urlparse(self.path)
                
            if path.path.rstrip('/') == '/register':
                print('Received data:', data)
                register_user(conn, cursor, data['username'], data['email'], data['password'])
                response_data = {"status": "success", "message": "Registration successful!"}

            elif path.path.rstrip('/') == '/login':
                response_data = login_user(conn, cursor, data['email'], data['password'])

            else:
                response_data = {"status": "error", "message": "Invalid endpoint"}

        except mysql.connector.Error as e:
            response_data = {"status": "error", 'message': f'Error connecting to database: {e}'}

        finally:
            #close the DB
            cursor.close()
            conn.close()

        #sending http response
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






