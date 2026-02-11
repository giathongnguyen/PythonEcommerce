from products import products
from access_control import check_access
from audit import log_event

orders = []

def calculate_discount(subtotal):
    if subtotal >= 1000:
        return 0.10
    elif subtotal >= 500:
        return 0.05
    return 0

def process_payment(amount):
    while True:
        choice = input(f"Confirm payment of ${amount}? (yes/no): ").lower()
        if choice in ["yes", "no"]:
            return choice == "yes"
        print("Invalid choice. Enter yes or no.")

def checkout(user):
    if not check_access(user, "customer"):
        return

    cart = {}

    while True:
        try:
            pid = int(input("Enter product ID (0 to checkout): "))
            if pid == 0:
                break

            product = next((p for p in products if p["product_id"] == pid), None)
            if product is None:
                print("Invalid product ID")
                log_event(f"Invalid product ID attempt: {pid}")
                continue

            qty = int(input("Enter quantity: "))
            if qty <= 0:
                print("Quantity must be positive")
                continue

            if pid in cart:
                if cart[pid] + qty > product["stock"]:
                    print("Insufficient stock")
                    continue
                cart[pid] += qty
            else:
                if qty > product["stock"]:
                    print("Insufficient stock")
                    continue
                cart[pid] = qty

            print("Cart updated")

        except ValueError:
            print("Invalid input")

    if not cart:
        print("Cart is empty")
        return

    subtotal = 0
    print("\n----- Cart Review -----")
    for pid, qty in cart.items():
        product = next(p for p in products if p["product_id"] == pid)
        item_total = product["price"] * qty
        subtotal += item_total
        print(f"{product['name']} x{qty} = ${item_total}")

    discount_rate = calculate_discount(subtotal)
    discount_amount = subtotal * discount_rate
    total = subtotal - discount_amount

    print("\n----- Order Summary -----")
    print("Subtotal:", subtotal)
    print("Discount:", discount_amount)
    print("Total:", total)

    if process_payment(total):
        confirm_order(user, cart, total)
    else:
        print("Payment cancelled")

def confirm_order(user, cart, total):
    for pid, qty in cart.items():
        product = next(p for p in products if p["product_id"] == pid)
        product["stock"] -= qty

    orders.append({
        "buyer": user["name"],
        "items": cart,
        "total": total,
        "status": "confirmed"
    })

    log_event(f"Order confirmed by {user['name']}, total ${total}")
    print("Order confirmed")

def view_orders(user):
    if not orders:
        print("No orders found.")
        return

    if user["role"] == "customer":
        user_orders = [o for o in orders if o["buyer"] == user["name"]]
        if not user_orders:
            print("No orders found.")
            return

        print(f"\n--- Orders for {user['name']} ---")
        for idx, o in enumerate(user_orders, 1):
            print(f"\nOrder #{idx} | Status: {o['status']} | Total: ${o['total']}")
            print(f"{'ID':<6}{'Name':<15}{'Quantity':<10}{'Total($)'}")
            print("-"*45)
            for pid, qty in o["items"].items():
                product = next(p for p in products if p["product_id"] == pid)
                item_total = product["price"] * qty
                print(f"{pid:<6}{product['name']:<15}{qty:<10}{item_total}")
            print("-"*45)

    elif user["role"] == "seller":
        print("\n--- Seller Order Management ---")
        for idx, o in enumerate(orders, 1):
            print(f"\nOrder #{idx} | Buyer: {o['buyer']} | Status: {o['status']} | Total: ${o['total']}")
            print(f"{'ID':<6}{'Name':<15}{'Quantity':<10}{'Total($)'}")
            print("-"*45)
            for pid, qty in o["items"].items():
                product = next(p for p in products if p["product_id"] == pid)
                item_total = product["price"] * qty
                print(f"{pid:<6}{product['name']:<15}{qty:<10}{item_total}")
            print("-"*45)

        try:
            order_idx = int(input("Enter order number to update status (0 to skip): "))
            if order_idx == 0:
                return
            if order_idx < 1 or order_idx > len(orders):
                print("Invalid order number")
                return

            new_status = input("Enter new status (processing/shipped/delivered): ").lower()
            if new_status not in ["processing", "shipped", "delivered"]:
                print("Invalid status")
                return

            orders[order_idx-1]["status"] = new_status
            log_event(f"Seller {user['name']} updated order {order_idx} to {new_status}")
            print(f"Order #{order_idx} status updated to {new_status}")

        except ValueError:
            print("Invalid input")

    elif user["role"] == "admin":
        print("\n--- All Orders ---")
        for idx, o in enumerate(orders, 1):
            print(f"\nOrder #{idx} | Buyer: {o['buyer']} | Status: {o['status']} | Total: ${o['total']}")
            print(f"{'ID':<6}{'Name':<15}{'Quantity':<10}{'Total($)'}")
            print("-"*45)
            for pid, qty in o["items"].items():
                product = next(p for p in products if p["product_id"] == pid)
                item_total = product["price"] * qty
                print(f"{pid:<6}{product['name']:<15}{qty:<10}{item_total}")
            print("-"*45)