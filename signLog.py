import hashlib
import json
import socketserver
import mysql.connector
import http.server

from mysql.connector import Error as MySQLerr


def register(conn, cursor, username, email, password):
    # Password hashing
    hash_pass = hashlib.sha256(password.encode()).hexdigest()

    # Inserting data into the users table
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hash_pass))
        conn.commit()
        return {"status": "success", "message": "Registration successful!"}
    except MySQLerr as e:
        if e.errno == 1062:  # MySQL error code for duplicate entry
            err_msg = str(e)

            if 'email' in err_msg:
                return {"status": "error", "message": "Email address is already in use. Please choose a different one."}
            elif 'username' in err_msg:  # Corrected typo: 'username' instead of 'user'
                return {"status": "error", "message": "Username is already in use. Please choose a different one."}
            else:
                return {"status": "error", "message": "An error occurred during registration."}
        
def login(conn, cursor, email, password):
    # Hashed password for comparison
    hash_pass = hashlib.sha256(password.encode()).hexdigest()
    
    # Retrieve user data from the database
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hash_pass))  # Corrected table name: 'users' instead of 'user'
    user = cursor.fetchone()

    if user:
        return {"status": "success", "message": "Login successful"}  # Added missing quotes around "success"
    else:
        return {"status": "failed", "message": "Invalid username or password"}  # Added missing quotes around "failed"
    
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if 'username' not in data or 'email' not in data or 'password' not in data:
            response_data = {"status": "error", "message": "Missing required fields"}
        else:
            # Connect to MySQL database
            try:
                print("Connecting to MySQL database...")
                conn = mysql.connector.connect(
                    host='127.0.0.1',
                    user='root',
                    password='1738',
                    database='lukoba'
                )

                if conn.is_connected():
                    print("Database connected successfully!")
                    cursor = conn.cursor()  # Cursor object to execute SQL queries

                    if self.path == '/register':
                        response_data = register(conn, cursor, data['username'], data['email'], data['password'])
                    elif self.path == '/login':
                        response_data = login(conn, cursor, data['email'], data['password'])

            except mysql.connector.Error as e:
                print(f"Database connection error: {e}")
                response_data = {"status": "error", "message": f"Database error: {e}"}

            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        print("Sending response...") 
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
