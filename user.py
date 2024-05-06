import psycopg2
from getpass import getpass

DATABASE = "YOUR_DATABASE"
USER = "YOUR_USER_NAME"
PASSWORD = "YOUR_PASSWORD"
HOST = "YOUR_DATABASE_HOST"

def connect_db():
    return psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)

def login():
    while True:
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = %s AND password_hash = crypt(%s, password_hash)", (username, password))
        user_id = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_id:
            return user_id[0]
        else:
            print("Login failed, please check your username and password and try again.")
