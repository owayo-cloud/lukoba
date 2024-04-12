import mysql.connector
import http.server
import json
from urllib.parse import urlparse
import logging
from admin import register_admin, login_admin
from user import register_user, login_user

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            path = urlparse(self.path)

            if path.path.startswith('/admin'):
                if path.path.rstrip('/') == '/admin/register':
                    response_data = register_admin(conn, cursor, data['username'], data['email'], data['password'], data['profilePicture'])
                elif path.path.rstrip('/') == '/admin/login':
                    response_data = login_admin(conn, cursor, data['email'], data['password'])
                else:
                    response_data = {"status": "error", "message": "Invalid admin endpoint"}

            elif path.path.startswith('/user'):
                if path.path.rstrip('/') == '/user/register':
                    response_data = register_user(conn, cursor, data['username'], data['email'], data['password'])
                elif path.path.rstrip('/') == '/user/login':
                    response_data = login_user(cursor, data['email'], data['password'])
                else:
                    response_data = {"status": "error", "message": "Invalid user endpoint"}
            else:
                response_data = {"status": "error", "message": "Invalid endpoint"}

        except mysql.connector.Error as e:
            logger.error("Database connection error: %s", e)
            response_data = {"status": "error", "message": "Database connection error."}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            return

        finally:
            cursor.close()
            conn.close()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

def main():
    PORT = 8000
    with http.server.HTTPServer(("", PORT), RequestHandler) as httpd:
        logger.info("Server started on port %s", PORT)
        httpd.serve_forever()

if __name__ == "__main__":
    main()

