from users import login
from products import filter_products_loop
from orders import checkout, view_orders
from audit import view_audit_log
from seller import seller_menu

print("=== E-Commerce Order Management System ===")

while True:
    user = login()
    if user is None:
        exit()

    if user["role"] == "customer":
        while user["logged_in"]:
            print("\n=== User Dashboard ===")
            print("1. Browse & Checkout")
            print("2. View My Orders")
            print("3. Exit")

            choice = input("Select an option: ")

            if choice == "1":
                filter_products_loop()
                checkout(user)

            elif choice == "2":
                view_orders(user)

            elif choice == "3":
                print("Goodbye!")
                user["logged_in"] = False
                break

            else:
                print("Invalid option. Try again.")

    elif user["role"] == "seller":
        while user["logged_in"]:
            seller_menu(user)

    elif user["role"] == "admin":
        while True:
            print("\n=== Admin Dashboard ===")
            print("1. View Audit Log")
            print("2. Exit")

            choice = input("Select option: ")

            if choice == "1":
                view_audit_log()
            elif choice == "2":
                print("Goodbye!")
                user["logged_in"] = False
                break
            else:
                print("Invalid option")