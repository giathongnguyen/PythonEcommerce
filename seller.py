from products import products, display_table
from orders import orders, view_orders
from audit import log_event

def seller_menu(user):
    while True:
        print("\n=== Seller Dashboard ===")
        print("1. List Products")
        print("2. Remove Product")
        print("3. Manage Product (update name/price)")
        print("4. View Store Orders")
        print("5. Update Order Status")
        print("6. Exit")

        choice = input("Select option: ")

        if choice == "1":
            display_table(products)

        elif choice == "2":
            # Remove product
            try:
                pid = int(input("Enter Product ID to remove: "))
                product = next((p for p in products if p["product_id"] == pid), None)
                if not product:
                    print("Invalid product ID")
                    log_event(f"Seller {user['name']} tried to remove invalid product ID: {pid}")
                    continue

                products.remove(product)
                print(f"Product {product['name']} removed")
                log_event(f"Seller {user['name']} removed product {product['name']}")

            except ValueError:
                print("Invalid input")


        elif choice == "3":
            try:
                pid = int(input("Enter Product ID to manage: "))
                product = next((p for p in products if p["product_id"] == pid), None)

                if not product:
                    print("Invalid product ID")
                    log_event(f"Seller {user['name']} tried to manage invalid product ID: {pid}")
                    continue

                new_name = input(f"Enter new name for {product['name']} (leave blank to keep): ")

                if new_name.strip():
                    product["name"] = new_name

                try:
                    new_price = input(f"Enter new price for {product['name']} (leave blank to keep): ")

                    if new_price.strip():
                        product["price"] = float(new_price)

                except ValueError:

                    print("Invalid price input")

                    continue

                print(f"Product updated: {product}")

                log_event(f"Seller {user['name']} updated product {product}")


            except ValueError:

                print("Invalid input")

        elif choice == "4":
            print("\n--- Store Orders ---")
            if not orders:
                print("No orders found.")
            else:
                for idx, o in enumerate(orders, 1):
                    seller_items = {pid: qty for pid, qty in o["items"].items() if
                                    any(p["product_id"] == pid for p in products)}
                    if seller_items:
                        print(f"\nOrder #{idx} | Buyer: {o['buyer']} | Status: {o['status']}")
                        print(f"{'ID':<6}{'Name':<15}{'Quantity':<10}{'Total($)'}")
                        print("-" * 45)
                        for pid, qty in seller_items.items():
                            product = next(p for p in products if p["product_id"] == pid)
                            item_total = product["price"] * qty
                            print(f"{pid:<6}{product['name']:<15}{qty:<10}{item_total}")
                        print("-" * 45)

        elif choice == "5":
            view_orders(user)

        elif choice == "6":
            print("Goodbye!")
            user["logged_in"] = False
            break

        else:
            print("Invalid option")
