from user import connect_db
from tabulate import tabulate

def create_account(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    account_name = input("Enter account name: ")
    account_type = input("Enter account type (Checking/Savings): ")
    balance = float(input("Enter initial balance: "))
    cursor.execute("INSERT INTO accounts (user_id, name, account_type, balance) VALUES (%s, %s, %s, %s)", (user_id, account_name, account_type, balance))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Account '{account_name}' created successfully!")

def list_accounts(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT account_id, name, account_type, balance FROM accounts WHERE user_id = %s", (user_id,))
    accounts = cursor.fetchall()
    if accounts:
        accounts_display = [[idx + 1, acc[1], acc[2], acc[3]] for idx, acc in enumerate(accounts)]
        print(tabulate(accounts_display, headers=['#', 'Name', 'Type', 'Balance'], tablefmt='grid'))
    else:
        print("No accounts found.")
    cursor.close()
    conn.close()

def delete_account(user_id):
    list_accounts(user_id)
    choice = int(input("Select which account # you would like to delete: "))
    confirm = input("Are you sure you want to delete this account? (yes/no): ")
    if confirm.lower() == 'yes':
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE account_id = %s", (choice,))
        cursor.execute("DELETE FROM accounts WHERE account_id = %s", (choice,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Account and associated transactions deleted successfully.")
