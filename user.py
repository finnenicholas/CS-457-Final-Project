from getpass import getpass
from db import connect_db
import account
import transaction

def user_operations(choice, user_id=None):
    if choice == 1:
        user_id = user_login()
        if user_id:
            print("Login successful!")
            return user_id
        else:
            print("Login failed, please try again.")
            return None
    elif choice == 2:
        user_id = create_user()
        if user_id:
            print("Account creation successful! Please log in.")
            return user_id
    elif choice == 3 and user_id:
        account.create_account(user_id)
    elif choice == 4 and user_id:
        transaction.record_transaction(user_id)
    elif choice == 5 and user_id:
        transaction.view_transactions(user_id)
    elif choice == 6 and user_id:
        account.list_accounts(user_id)
    elif choice == 7 and user_id:
        account.delete_account(user_id)
    elif choice == 8 and user_id:
        transaction.delete_transaction(user_id)

def user_login():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = %s AND password_hash = crypt(%s, password_hash)", (username, password))
    user_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_id[0] if user_id else None

def create_user():
    username = input("Enter a new username: ")
    password = getpass("Enter a new password: ")
    email = input("Enter your email: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, crypt(%s, gen_salt('bf')), %s) RETURNING user_id", (username, password, email))
    user_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return user_id[0] if user_id else None
