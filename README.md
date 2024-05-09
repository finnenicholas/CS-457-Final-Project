## Introduction

# CS-457-Final-Project
My stonks project for UNR CS 457 Database systems

# Stock Transaction Manager Application

**Creator:** Nicholas Finne

**Description:**  
The Stock Transaction Manager is an application designed to help users manage their financial transactions related to stock trading efficiently. It allows users to create and manage accounts, record buy and sell transactions, view transactions per account, and delete transactions or accounts.

Have a file called db.py with all your database connection info.

## Tutorial

### How to Use This Application:

1. **Start the Application:**
   - Navigate to the application directory.
   - Run the command `python main.py` in your terminal.

2. **Login or Create Account:**
   - Login with your credentials or create a new user account if using for the first time.

3. **Navigating the Menu:**
   - **Create an Account:** Set up a new account for tracking transactions.
   - **Record a Transaction:** Enter new stock transaction details.
   - **View Accounts:** See all your accounts and their details.
   - **View Transactions:** Select an account to view its specific transactions.
   - **Delete an Account:** Remove an account and all its associated transactions.
   - **Delete a Transaction:** Remove a particular transaction from an account.
   - **Exit:** Terminate the application session.

4. **Performing Actions:**
   - Follow the on-screen prompts to provide necessary details for each action (e.g., account creation, transaction recording).

## Libraries

- **psycopg2:** Facilitates interaction with PostgreSQL databases, allowing CRUD operations on the system's database.
- **getpass:** Used to securely handle password input without displaying it on the screen.
- **datetime:** Provides tools for manipulating dates and times, which is essential for transaction timestamping.
- **alpha_vantage:** Integrates with the Alpha Vantage API to fetch real-time stock price data.
- **pandas:** Handles data in tabular form, simplifying data manipulation and analysis.
- **tabulate:** Enhances CLI outputs by formatting tabular data into easy-to-read grid-style tables.

## Help

### Resources and Links:

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)
- [Python Official Documentation](https://docs.python.org/3/)
