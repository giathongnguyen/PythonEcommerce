def check_access(user, required_role):
    if not user["logged_in"]:
        print("Access denied: Not logged in")
        return False
    if user["status"] != "active":
        print("Access denied: Account inactive")
        return False
    if user["role"] != required_role:
        print("Access denied: Permission denied")
        return False

    print(f"Access granted ({required_role})")
    return True
