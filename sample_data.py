import mysql.connector

def insert_sample_data():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            username='root',
            password='1738',
            database='lukoba' 
        )
        cursor = conn.cursor()

        # Insert sample movies
        cursor.executemany('''
            INSERT INTO movies (title, description, rating, duration, genre, image_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', [
            ("Movie 1", "Description 1", "PG", 120, "Action", "url1"),
            ("Movie 2", "Description 2", "R", 90, "Comedy", "url2"),
            ("Movie 3", "Description 3", "PG-13", 150, "Drama", "url3")
        ])

        # Insert sample showtimes
        cursor.executemany('''
            INSERT INTO showtimes (movie_id, start_time)
            VALUES (%s, %s)
        ''', [
            (1, "2024-06-01 14:00:00"),
            (1, "2024-06-01 17:00:00"),
            (2, "2024-06-02 15:00:00"),
            (3, "2024-06-03 20:00:00")
        ])

        # Insert sample users
        cursor.executemany('''
            INSERT INTO users (username, password, email)
            VALUES (%s, %s, %s)
        ''', [
            ("user1", "password1", "user1@example.com"),
            ("user2", "password2", "user2@example.com")
        ])

        conn.commit()
        cursor.close()
        conn.close()

        print("Sample data inserted successfully.")
    except mysql.connector.Error as err:
        print(err)
    else:
        conn.close()

if __name__ == '__main__':
    insert_sample_data()
