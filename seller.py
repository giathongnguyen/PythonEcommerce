from products import products, display_table
from audit import log_event

def seller_menu(user):
    while True:
        print("\n=== Seller Dashboard ===")
        print("1. List Products")
        print("2. Update Stock")
        print("3. Exit")

        choice = input("Select option: ")

        if choice == "1":
            display_table(products)

        elif choice == "2":
            try:
                pid = int(input("Enter Product ID to update stock: "))
                product = next((p for p in products if p["product_id"] == pid), None)

                if product is None:
                    print("Invalid product ID")
                    log_event(f"Seller {user['name']} tried invalid product ID: {pid}")
                    continue

                qty = int(input(f"Enter new stock quantity for {product['name']}: "))
                if qty < 0:
                    print("Stock cannot be negative")
                    continue

                product["stock"] = qty
                print(f"Stock updated: {product['name']} now has {qty} units")
                log_event(f"Seller {user['name']} updated stock for {product['name']} to {qty}")

            except ValueError:
                print("Invalid input")

        elif choice == "3":
            print("Goodbye!")
            user["logged_in"] = False
            break

        else:
            print("Invalid option")
