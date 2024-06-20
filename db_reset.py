import mysql.connector
import logging

def clear_and_reset_db():
    try:
        #connecting to the DB
        conn = mysql.connector.connect(
            host = 'localhost',
            username = 'root',
            password = '1738',
            database = 'lCinema'
        )
        cursor = conn.cursor()
        print('Connection to the database successful')

        #deleting data from the tables
        cursor.execute("DELETE FROM movies")

        #reset the auto increment to 1
        cursor.execute("ALTER TABLE movies AUTO_INCREMENT = 1")

        #Commit changes and exit the DB
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