users = [
    {"user_id": 1,
     "name": "Alice",
     "email": "alice@gmail.com",
     "password": "1234",
     "role": "customer",
     "logged_in": False,
     "status": "active"},
    {"user_id": 2,
     "name": "Bob",
     "email": "bob@gmail.com",
     "password": "abcd",
     "role": "seller",
     "logged_in": False,
     "status": "active"},
    {"user_id": 3,
     "name": "Admin",
     "email": "admin@gmail.com",
     "password": "admin",
     "role": "admin",
     "logged_in": False,
     "status": "active"}
]

def login():
    while True:
        email = input("Enter email (or type 'exit' to quit): ")
        if email.lower() == "exit":
            print("Exiting login.")
            return None

        password = input("Enter password: ")

        for user in users:
            if user["email"] == email and user["password"] == password:
                user["logged_in"] = True
                print("Login successful")
                return user

        print("Login failed please try again.")

