import mysql.connector
import logging

def clear_and_reset_db():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host='localhost',
            username='root',
            password='1738',
            database='lukoba'
        )
        cursor = conn.cursor()

        # Delete all data from the tables
        cursor.execute("DELETE FROM movies")
        # Add more delete statements for other tables if needed

        # Reset auto-increment for the users table
        cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1")

        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()

        logging.info("Database cleared and reset successfully!")
    except mysql.connector.Error as e:
        logging.error("Database error: %s", e)
    except Exception as ex:
        logging.error("Unexpected error occurred: %s", ex)

if __name__ == "__main__":
    clear_and_reset_db()
