import mysql.connector
import bcrypt
from http import cookies

def register_admin(conn, cursor, username, email, password, profilePicture):
    try:
        # Hash password using bcrypt
        hash_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        # Insert user data into DB
        cursor.execute("INSERT INTO admin (username, email, password, profilePicture) VALUES (%s, %s, %s, %s)", (username, email, hash_pass, profilePicture))
        conn.commit()
        return {"status": "success", "message": "Registration successful!"}
    except mysql.connector.Error as e:
        return {"status": "error", "message": "Registration failed."}

def login_admin(conn, cursor, email, password):
    try:
        # Check if admin with given email exists in DB
        cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            # Verify password using bcrypt
            if bcrypt.checkpw(password.encode(), user[2].encode()):
                # Setting cookie upon successful login
                cookie = cookies.SimpleCookie()
                cookie['admin_email'] = email
                cookie['admin_email']['path'] = '/'
                cookie['admin_email']['httponly'] = True
                return {"status": "success", "message": "Login successful!", "cookie": cookie.output(header='')}
            else:
                return {"status": "error", "message": "Invalid email or password."}
        else:
            return {"status": "error", "message": "Invalid email or password."}
    except mysql.connector.Error as e:
        return {"status": "error", "message": "Login failed."}
