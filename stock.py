def fetch_or_create_stock(ticker_symbol):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT stock_id FROM stocks WHERE ticker_symbol = %s", (ticker_symbol,))
    stock_id = cursor.fetchone()
    if stock_id:
        return stock_id[0]
    else:
        cursor.execute("INSERT INTO stocks (ticker_symbol) VALUES (%s) RETURNING stock_id", (ticker_symbol,))
        stock_id = cursor.fetchone()[0]
        conn.commit()
        return stock_id