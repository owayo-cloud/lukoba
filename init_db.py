import mysql.connector
from mysql.connector import errorcode

def init_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            username='root',
            password='1738',
            database='lukoba'     
        )
        cursor = conn.cursor()

        with open('schema.sql', 'r') as f:
            schema = f.read()

        for statement in schema.split(';'):
            if statement.strip():
                cursor.execute(statement)

        conn.commit()
        cursor.close()
        conn.close()

        print("Database initialized successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        conn.close()

if __name__ == '__main__':
    init_db()