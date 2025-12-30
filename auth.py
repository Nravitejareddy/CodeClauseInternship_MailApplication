import hashlib
from database import cursor, conn

def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password):
    """Register a new user"""
    try:
        cursor.execute(
            "INSERT INTO users(username, password) VALUES (?,?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except:
        return False  # User already exists

def login(username, password):
    """Login user and return user_id"""
    cursor.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    result = cursor.fetchone()
    return result[0] if result else None
