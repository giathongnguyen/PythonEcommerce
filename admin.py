from users import users
from products import products, display_table
from orders import orders
from audit import log_event, view_audit_log
from discounts import discount_rules

def manage_users():
    print("\n--- Manage Users ---")
    print(f"{'ID':<5}{'Name':<15}{'Role':<10}{'Status'}")
    print("-" * 40)

    for u in users:
        print(f"{u['user_id']:<5}{u['name']:<15}{u['role']:<10}{u['status']}")

    try:
        uid = int(input("\nEnter User ID to update status (0 to cancel): "))
        if uid == 0:
            return

        user = next((u for u in users if u["user_id"] == uid), None)
        if not user:
            print("Invalid user ID")
            log_event(f"Admin attempted invalid user ID: {uid}")
            return

        new_status = input("Enter new status (active/suspended): ").lower()
        if new_status not in ["active", "suspended"]:
            print("Invalid status")
            return

        user["status"] = new_status
        log_event(f"Admin changed status of {user['name']} to {new_status}")
        print("User status updated")

    except ValueError:
        print("Invalid input")


def manage_products():
    print("\n--- Manage Products ---")
    display_table(products)

    try:
        pid = int(input("Enter Product ID to remove (0 to cancel): "))
        if pid == 0:
            return

        product = next((p for p in products if p["product_id"] == pid), None)
        if not product:
            print("Invalid product ID")
            log_event(f"Admin attempted invalid product ID: {pid}")
            return

        products.remove(product)
        log_event(f"Admin removed product {product['name']}")
        print("Product removed successfully")

    except ValueError:
        print("Invalid input")


def view_all_orders():
    if not orders:
        print("No orders found.")
        return

    print("\n--- All Orders ---")
    for idx, o in enumerate(orders, 1):
        print(f"\nOrder #{idx} | Buyer: {o['buyer']} | Status: {o['status']} | Total: ${o['total']}")
        print(f"{'ID':<6}{'Name':<15}{'Qty':<8}{'Total($)'}")
        print("-" * 45)

        for pid, qty in o["items"].items():
            product = next(p for p in products if p["product_id"] == pid)
            item_total = product["price"] * qty
            print(f"{pid:<6}{product['name']:<15}{qty:<8}{item_total}")

        print("-" * 45)


def manage_discount_rules():
    print("\n--- Manage Discount Rules ---")

    for k, v in discount_rules.items():
        print(f"{k}: Orders ≥ ${v['min_total']} → {int(v['rate']*100)}% OFF")

    try:
        tier = input("Select tier to edit (tier1/tier2 or 0 to cancel): ").lower()
        if tier == "0":
            return

        if tier not in discount_rules:
            print("Invalid tier")
            return

        min_total = int(input("New minimum total: "))
        rate = float(input("New discount rate (0.1 = 10%): "))

        if min_total <= 0 or rate <= 0 or rate >= 1:
            print("Invalid values")
            return

        discount_rules[tier]["min_total"] = min_total
        discount_rules[tier]["rate"] = rate
        log_event(f"Admin updated discount rule {tier}")

        print("Discount rule updated")

    except ValueError:
        print("Invalid input")

def admin_menu(user):
    while True:
        print("\n=== Admin Dashboard ===")
        print("1. Manage Users")
        print("2. Manage Products")
        print("3. View Orders")
        print("4. Manage Discount Rules")
        print("5. View Audit Log")
        print("6. Exit")

        choice = input("Select option: ")

        if choice == "1":
            manage_users()

        elif choice == "2":
            manage_products()

        elif choice == "3":
            view_all_orders()

        elif choice == "4":
            manage_discount_rules()

        elif choice == "5":
            view_audit_log()

        elif choice == "6":
            print("Goodbye!")
            user["logged_in"] = False
            break

        else:
            print("Invalid option")