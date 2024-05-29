import mysql.connector
import hashlib
import logging

def hash_password(password):
    sha256_hash = hashlib.sha256() # Create a SHA-256 hash object
    sha256_hash.update(password.encode()) # Update the hash object with the password bytes
    
    hashed_password = sha256_hash.hexdigest() # Get the hashed password as a hexadecimal string
    
    return hashed_password

def register_user(conn, cursor, username, email, password):
    try:
        # Hash the password
        hash_pass = hash_password(password)
        # Store the hashed password directly in the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hash_pass))
        conn.commit()
        return {"status": "success", "message": "Registration successful!"}
    except mysql.connector.Error as e:
        return {"status": "error", "message": "Registration failed."}

def login_user(cursor, email, password):
    try:
        cursor.execute("SELECT email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            stored_email = user[0]
            stored_password_hash = user[1]
            if stored_password_hash == hash_password(password):
                return {"status": "success", "message": "Login successful!"}
            else:
                logging.error("Invalid password for user: %s", email)
                return {"status": "error", "message": "Invalid email or password."}
        else:
            logging.error("User not found for email: %s", email)
            return {"status": "error", "message": "Invalid email or password."}
    except mysql.connector.Error as e:
        logging.error("Database error: %s", e)
        return {"status": "error", "message": "Login failed due to database error."}
    except Exception as ex:
        logging.error("Unexpected error occurred: %s", ex)
        return {"status": "error", "message": "Unexpected error occurred during login."}
