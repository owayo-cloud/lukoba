import mysql.connector
import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
import logging
from user import register_user, login_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#import stripe
#Stripe API key setup
#stripe.api_key = "sk_test_51PLkYeP0uauYxIKVN5samJstvABm4A06IYCdnZkbrA35kHPs3SYithn1wucxtNsXdcqO34ogOYHSDm4c3prLDtrE00eqOl8GP9"


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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        try:
            conn = mysql.connector.connect(
                host='localhost',
                username='root',
                password='1738',
                database='lukoba'
            )
            cursor = conn.cursor()
        except mysql.connector.Error as e:
            logger.error("Database connection error: %s", e)
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {"status": "error", "message": "Database connection error."}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            return

        path = urlparse(self.path).path

        if path == '/user/register':
            is_admin = data.get('is_admin', False)
            response_data = register_user(conn, cursor, data['username'], data['email'], data['password'], is_admin)
        elif path == '/user/login':
            response_data = login_user(cursor, data['email'], data['password'])
        else:
            response_data = {"status": "error", "message": "Invalid endpoint"}

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