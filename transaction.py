from alpha_vantage.timeseries import TimeSeries
from user import connect_db
from tabulate import tabulate
import account

API_KEY = 'API_KEY'

def record_transaction(user_id):
    account.list_accounts(user_id)
    account_id = int(input("Select which account # you would like to use: "))
    ticker_symbol = input("Enter ticker symbol: ")
    quantity = int(input("Enter quantity: "))
    transaction_type = input("Enter transaction type (buy/sell): ")
    transaction_date = input("Enter transaction date (YYYY-MM-DD): ")
    transaction_time = input("Enter transaction time (HH:MM): ")

    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data, _ = ts.get_quote_endpoint(symbol=ticker_symbol)
    price_at_transaction = float(data['05. price'].iloc[0]) if '05. price' in data else None
    if not price_at_transaction:
        print("Failed to fetch valid price data from API.")
        return
    print(f"Fetched price for {ticker_symbol}: {price_at_transaction}")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (account_id, ticker_symbol, quantity, price_at_transaction, transaction_date, transaction_time, transaction_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (account_id, ticker_symbol, quantity, price_at_transaction, transaction_date, transaction_time, transaction_type))
    conn.commit()
    cursor.close()
    conn.close()
    print("Transaction recorded successfully.")

def view_transactions(user_id):
    account.list_accounts(user_id)
    account_id = int(input("Select which account # you would like to view the transactions of: "))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT transaction_id, transaction_date, transaction_time, transaction_type, s.ticker_symbol, t.quantity, t.price_at_transaction FROM transactions t JOIN stocks s ON t.stock_id = s.stock_id WHERE t.account_id = %s ORDER BY transaction_date, transaction_time", (account_id,))
    transactions = cursor.fetchall()
    if transactions:
        transactions_display = [[idx + 1, tran[1], tran[2], tran[3], tran[4], tran[5], tran[6]] for idx, tran in enumerate(transactions)]
        print(tabulate(transactions_display, headers=['#', 'Date', 'Time', 'Type', 'Symbol', 'Quantity', 'Price'], tablefmt='grid'))
        cursor.close()
        conn.close()
        return True
    else:
        print("There are no transactions to view.")
        cursor.close()
        conn.close()
        return False

def delete_transaction(user_id):
    # Display the user's accounts and prompt to choose one for deleting a transaction
    account.list_accounts(user_id)
    account_id = int(input("Select which account # you would like to delete the transaction from: "))

    # Display the transactions from the chosen account
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT transaction_id, transaction_date, transaction_time, transaction_type, s.ticker_symbol, t.quantity, t.price_at_transaction FROM transactions t JOIN stocks s ON t.stock_id = s.stock_id WHERE t.account_id = %s ORDER BY transaction_date, transaction_time", (account_id,))
    transactions = cursor.fetchall()
    
    if transactions:
        # Format and display transactions
        transactions_display = [[idx + 1, tran[1], tran[2], tran[3], tran[4], tran[5], tran[6]] for idx, tran in enumerate(transactions)]
        print(tabulate(transactions_display, headers=['#', 'Date', 'Time', 'Type', 'Symbol', 'Quantity', 'Price'], tablefmt='grid'))
        
        # User selects a transaction to delete
        transaction_num = int(input("Select which transaction # you would like to delete: "))
        if 1 <= transaction_num <= len(transactions):
            transaction_id = transactions[transaction_num - 1][0]
            confirm = input("Are you sure you want to delete this transaction? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM transactions WHERE transaction_id = %s", (transaction_id,))
                conn.commit()
                print("Transaction deleted successfully.")
            else:
                print("Transaction deletion canceled.")
        else:
            print("Invalid transaction number selected.")
    else:
        print("No transactions available to delete.")
    
    cursor.close()
    conn.close()