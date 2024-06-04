import mysql.connector
import hashlib
import logging

logger = logging.getLogger(__name__)

def register_user(conn, cursor, username, email, password,is_admin=False):
    try:
        # Hash the password
        hash_pass = hashlib.sha256(password.encode()).hexdigest()
        # Store the hashed password directly in the database
        cursor.execute("INSERT INTO users (username, email, password, is_admin) VALUES (%s, %s, %s, %s)", (username, email, hash_pass, is_admin))
        conn.commit()
        return {"status": "success", "message": "Registration successful!"}
    except mysql.connector.Error as e:
        logger.error("Error registering user: %s", e)
        return {"status": "error", "message": str(e)}

def login_user(cursor, email, password):
    try:
        hash_pass = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, hash_pass))
        user = cursor.fetchone()
        if user:
            logger.info("User found: %s", user)
            return {"status": "success", "message": "Login successful", "user": {"id": user[0], "username": user[1], "email": user[2], "is_admin": user[4]}} 
        else:
            logger.warning("Invalid login attempt for email: %s", email)
            return {"status": "error", "message": "Invalid email or password."}
    except mysql.connector.Error as e:
        logger.error("Error logging in user: %s", e)
        return {"status": "error", "message": str(e)}