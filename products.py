products = [
    {"product_id": 101, "name": "Laptop", "price": 1000, "stock": 5},
    {"product_id": 102, "name": "Mouse", "price": 50, "stock": 20},
    {"product_id": 103, "name": "Keyboard", "price": 80, "stock": 10}
]

def get_discount_offer(price):
    if price >= 1000:
        return "10% OFF"
    elif price >= 500:
        return "5% OFF"
    else:
        return "No discount"

def display_table(product_list):
    print("\n---------------------------------------------------------------")
    print(f"{'ID':<6}{'Product':<15}{'Price($)':<12}{'Stock':<10}{'Discount'}")
    print("---------------------------------------------------------------")

    for p in product_list:
        discount = get_discount_offer(p["price"])
        print(f"{p['product_id']:<6}{p['name']:<15}{p['price']:<12}{p['stock']:<10}{discount}")

    print("---------------------------------------------------------------")

def filter_products_loop():
    print("\nAvailable Products:")
    display_table(products)

    while True:
        try:
            max_price = int(input(
                "\nEnter max price to filter "
                "(0 = no filter, -1 = exit): "
            ))

            if max_price == -1:
                print("Exiting product filter.")
                break

            if max_price < -1:
                print("Invalid input. Try again.")
                continue

            if max_price == 0:
                filtered = products
            else:
                filtered = [p for p in products if p["price"] <= max_price]

            if not filtered:
                print("No products found. Try again.")
                continue

            display_table(filtered)

        except ValueError:
            print("Please enter a valid number.")
