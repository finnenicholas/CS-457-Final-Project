import user
import account
import transaction

def main():
    print("Welcome to Stock Transaction Manager")
    user_id = user.login()
    if user_id:
        print("Login successful!")
        account.list_accounts(user_id)
        while True:
            print("\n1. Create an account")
            print("2. Record a transaction")
            print("3. View accounts")
            print("4. View transactions")
            print("5. Delete an account")
            print("6. Delete a transaction")
            print("7. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
                account.create_account(user_id)
            elif choice == '2':
                transaction.record_transaction(user_id)
            elif choice == '3':
                account.list_accounts(user_id)
            elif choice == '4':
                transaction.view_transactions(user_id)
            elif choice == '5':
                account.delete_account(user_id)
            elif choice == '6':
                transaction.delete_transaction(user_id)
            elif choice == '7':
                break
    else:
        print("Login failed, please check your username and password.")

if __name__ == "__main__":
    main()
