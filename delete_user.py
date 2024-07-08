import sqlite3

def delete_user(email):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('lCinema.sqlite3')

        # Create a cursor object
        cursor = conn.cursor()

        # Delete user by email
        cursor.execute('DELETE FROM users WHERE email = ?', (email,))

        # Check if the user was deleted
        if cursor.rowcount == 0:
            print(f"No user found with email: {email}")
        else:
            print(f"User with email {email} deleted successfully.")

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        print("Failed to delete user from SQLite table", error)

# Example usage
delete_user('newuser@example.com')
