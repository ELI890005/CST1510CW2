import bcrypt
from database import db

def register_user(username, password, role):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    db.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, hashed_pw, role),
        commit=True
    )

def verify_user(username, password):
    user = db.fetch_one("SELECT * FROM users WHERE username = ?", (username,))

    if not user:
        return False, None

    stored_hash = user["password_hash"]

    if bcrypt.checkpw(password.encode(), stored_hash):
        return True, user

    return False, None
