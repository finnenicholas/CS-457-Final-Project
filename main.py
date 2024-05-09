from user import user_operations, user_login, create_user

def main_menu():
    print("\nWelcome to the Stock Transaction Manager")
    print("1. Login")
    print("2. Create an Account")
    user_choice = input("Enter choice (1-2): ")
    if user_choice == '1':
        user_id = user_login()
        if user_id:
            user_operations_menu(user_id)
    elif user_choice == '2':
        user_id = create_user()
        if user_id:
            user_operations_menu(user_id)

def user_operations_menu(user_id):
    while True:
        print("\nSelect an operation:")
        print("3. Add Bank Account")
        print("4. Record a transaction")
        print("5. View transactions")
        print("6. View accounts")
        print("7. Delete an account")
        print("8. Delete a transaction")
        print("9. Exit")
        choice = input("Enter choice (3-9): ")
        if choice == '9':
            break
        user_operations(int(choice), user_id)

def main():
    main_menu()

if __name__ == "__main__":
    main()
