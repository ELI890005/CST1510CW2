import bcrypt
import os

USERS_FILE = "users.txt"


def hash_password(plain_password: str) -> bytes:
    """
    Take a plain-text password and return a bcrypt hash.
    """
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """
    Check if a plain-text password matches the stored bcrypt hash.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)


def load_users():
    """
    Read all users from users.txt and return a dict:
    {
        "username": {"hash": b"...", "role": "cyber_analyst"}
    }
    """
    users = {}

    if not os.path.exists(USERS_FILE):
        return users

    with open(USERS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # username,hash,role
            parts = line.split(",")
            if len(parts) != 3:
                continue
            username, hashed_str, role = parts
            users[username] = {
                "hash": hashed_str.encode("utf-8"),
                "role": role,
            }
    return users


def save_user(username: str, hashed_password: bytes, role: str):
    """
    Append a new user to users.txt
    """
    with open(USERS_FILE, "a") as f:
        line = f"{username},{hashed_password.decode('utf-8')},{role}\n"
        f.write(line)


def register_user():
    """
    Register a new user with a role.
    """
    users = load_users()

    print("\n=== Register New User ===")
    username = input("Choose a username: ").strip()

    if username in users:
        print(" That username already exists. Try another one.\n")
        return

    password = input("Choose a password: ").strip()
    confirm = input("Confirm password: ").strip()

    if password != confirm:
        print(" Passwords do not match.\n")
        return

    print("\nChoose a role for this user:")
    print("1) cyber_analyst")
    print("2) it_admin")
    print("3) data_scientist")

    role_choice = input("Enter 1, 2, or 3: ").strip()
    roles = {"1": "cyber_analyst", "2": "it_admin", "3": "data_scientist"}
    role = roles.get(role_choice, "cyber_analyst")

    hashed = hash_password(password)
    save_user(username, hashed, role)

    print(f"\n User '{username}' registered with role '{role}'.\n")


def login_user():
    """
    Login an existing user by checking the hashed password.
    """
    users = load_users()

    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username not in users:
        print(" Invalid username or password.\n")
        return

    user_record = users[username]
    hashed = user_record["hash"]

    if verify_password(password, hashed):
        print(f"\n Login successful! Welcome, {username}.")
        print(f"   Your role is: {user_record['role']}\n")
    else:
        print(" Invalid username or password.\n")


def main_menu():
    """
    Simple text menu to register or login.
    """
    while True:
        print("=== CST1510 Auth System ===")
        print("1) Register")
        print("2) Login")
        print("3) Exit")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print(" Invalid option. Try again.\n")


if __name__ == "__main__":
    main_menu()
