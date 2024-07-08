import sqlite3

def connect_db():
    return sqlite3.connect('lCinema.sqlite3')

def create_user(email, password, username):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Insert user into the database
        cursor.execute('INSERT INTO users (email, password, username) VALUES (?, ?, ?)', (email, password, username))
        
        conn.commit()
        print(f"User with email {email} created successfully.")
    except sqlite3.IntegrityError as error:
        print(f"Failed to create user: {error}")
    finally:
        conn.close()

def edit_user(email, new_email=None, new_password=None, new_username=None):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Update user information based on provided parameters
        if new_email:
            cursor.execute('UPDATE users SET email = ? WHERE email = ?', (new_email, email))
        if new_password:
            cursor.execute('UPDATE users SET password = ? WHERE email = ?', (new_password, email))
        if new_username:
            cursor.execute('UPDATE users SET username = ? WHERE email = ?', (new_username, email))

        if cursor.rowcount == 0:
            print(f"No user found with email: {email}")
        else:
            print(f"User with email {email} updated successfully.")

        conn.commit()
    except sqlite3.Error as error:
        print(f"Failed to edit user: {error}")
    finally:
        conn.close()

def delete_user(email):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Delete user by email
        cursor.execute('DELETE FROM users WHERE email = ?', (email,))

        if cursor.rowcount == 0:
            print(f"No user found with email: {email}")
        else:
            print(f"User with email {email} deleted successfully.")

        conn.commit()
    except sqlite3.Error as error:
        print(f"Failed to delete user: {error}")
    finally:
        conn.close()

# Example usage
if __name__ == "__main__":
    # Create a user
    create_user('akeno@gmail.com', 'Password123', 'newuser')

    # Edit a user
    #edit_user('newuser@example.com', new_email='editeduser@example.com', new_password='NewPassword456', new_username='editeduser')

    # Delete a user
    #delete_user('editeduser@example.com')
