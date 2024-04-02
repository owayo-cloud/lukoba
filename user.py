#connecting sql to database
import hashlib
import http.server
import json
import socketserver
import mysql.connector
from mysql.connector import Error as MySQLError


# Connect to MySQL database
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='1738',
    database='omtbs'
)
c = conn.cursor()

def register(username, email, password):
    #hashing the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    #inserting data into the database
    try:
        c.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        conn.commit()
        return {"status": "success", "message": "Registration successful!"}
    except MySQLError as e:
        if e.errno == 1062: # MySQL error code for duplicate entry
            error_msg = str(e)

        if "email" in error_msg:
            return {"status": "error", "message": "Email address is already in use. Please choose a different one."}
        elif "username" in error_msg:
            return {"status": "error", "message": "Username is already in use. Please choose a different one."}
        else:
            return {"status": "error", "message": "An error occurred during registration."}
def login(email, password):
    #hashed password for comparison
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    #retrieve user data from the database
    c.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, hashed_password))
    user = c.fetchone()

    if user:
        return{"status": "success", "message": "Login successful"}
    else:
        return{"status":"failed", "message":"Invalid username or password"}
    
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if 'username' not in data or 'email' not in data or 'password' not in data:
            response_data = {"status": "error", "message": "Missing required fields"}
        else:
            if self.path == 'http://localhost:8000/register':
                response_data = register(data['username'], data['email'], data['password'])
            elif self.path == 'http://localhost:8000/login':
                response_data = login(data['email'], data['password'])
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    PORT = 8080
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print("Server started on port", PORT)
        httpd.serve_forever()

if __name__ == "__main__":
    main()

# Close the database connection when done
conn.close()
    
