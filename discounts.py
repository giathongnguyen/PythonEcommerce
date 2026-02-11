discount_rules = {
    "tier1": {"min_total": 500, "rate": 0.05},
    "tier2": {"min_total": 1000, "rate": 0.10}
}

def calculate_discount(subtotal):
    discount = 0
    for rule in discount_rules.values():
        if subtotal >= rule["min_total"]:
            discount = max(discount, rule["rate"])
    return discount