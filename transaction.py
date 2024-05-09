from alpha_vantage.timeseries import TimeSeries
from tabulate import tabulate
import account
from db import connect_db

API_KEY = 'T1ZYRW6D4LYKMJK0'

def record_transaction(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT account_id, name, account_type, balance FROM accounts WHERE user_id = %s", (user_id,))
    accounts = cursor.fetchall()
    if not accounts:
        print("No accounts found.")
        cursor.close()
        conn.close()
        return

    accounts_display = [[idx + 1, acc[1], acc[2], f"{acc[3]:.2f}"] for idx, acc in enumerate(accounts)]
    print(tabulate(accounts_display, headers=['#', 'Name', 'Type', 'Balance'], tablefmt='grid'))

    choice = int(input("Select which account # you would like to use by number: "))
    if choice < 1 or choice > len(accounts):
        print("Invalid choice. Please try again.")
        cursor.close()
        conn.close()
        return
    
    account_id = accounts[choice-1][0]

    ticker_symbol = input("Enter ticker symbol: ")
    quantity = int(input("Enter quantity: "))
    transaction_type = input("Enter transaction type (buy/sell): ")
    transaction_date = input("Enter transaction date (YYYY-MM-DD): ")
    transaction_time = input("Enter transaction time (HH:MM): ")

    cursor.execute("SELECT stock_id FROM stocks WHERE ticker_symbol = %s", (ticker_symbol,))
    stock_id = cursor.fetchone()
    if not stock_id:
        print("Stock symbol not found. Please make sure it's correct.")
        cursor.close()
        conn.close()
        return
    stock_id = stock_id[0]

    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data, _ = ts.get_quote_endpoint(symbol=ticker_symbol)
    price_at_transaction = float(data['05. price'].iloc[0]) if '05. price' in data else None
    if not price_at_transaction:
        print("Failed to fetch valid price data from API.")
        cursor.close()
        conn.close()
        return

    print(f"Fetched price for {ticker_symbol}: {price_at_transaction}")

    cursor.execute("INSERT INTO transactions (account_id, stock_id, quantity, price_at_transaction, transaction_date, transaction_time, transaction_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (account_id, stock_id, quantity, price_at_transaction, transaction_date, transaction_time, transaction_type))
    conn.commit()
    cursor.close()
    conn.close()
    print("Transaction recorded successfully.")

def view_transactions(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT account_id, name, account_type, balance FROM accounts WHERE user_id = %s", (user_id,))
    accounts = cursor.fetchall()
    if not accounts:
        print("No accounts found.")
        cursor.close()
        conn.close()
        return

    accounts_display = [[idx + 1, acc[1], acc[2], f"{acc[3]:.2f}"] for idx, acc in enumerate(accounts)]
    print(tabulate(accounts_display, headers=['#', 'Name', 'Type', 'Balance'], tablefmt='grid'))

    account_number = int(input("Select which account # you would like to view the transactions of: "))
    if account_number < 1 or account_number > len(accounts):
        print("Invalid account number. Please try again.")
        cursor.close()
        conn.close()
        return

    account_id = accounts[account_number-1][0]

    cursor.execute("SELECT transaction_id, transaction_date, transaction_time, transaction_type, s.ticker_symbol, t.quantity, t.price_at_transaction FROM transactions t JOIN stocks s ON t.stock_id = s.stock_id WHERE t.account_id = %s ORDER BY transaction_date, transaction_time", (account_id,))
    transactions = cursor.fetchall()
    if transactions:
        transactions_display = [[idx + 1, tran[1], tran[2], tran[3], tran[4], tran[5], tran[6]] for idx, tran in enumerate(transactions)]
        print(tabulate(transactions_display, headers=['#', 'Date', 'Time', 'Type', 'Symbol', 'Quantity', 'Price'], tablefmt='grid'))
    else:
        print("There are no transactions to view.")
    cursor.close()
    conn.close()

def delete_transaction(user_id):
    view_transactions(user_id)
    transaction_number = int(input("Select which transaction # you would like to delete: "))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE transaction_id = %s", (transaction_number,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Transaction deleted successfully.")
