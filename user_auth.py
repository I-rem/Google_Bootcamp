import json
import os
import hashlib

USER_FILE = "users.json"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    try:
        with open(USER_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def user_exists(username):
    users = load_users()
    return username in users

def register(username, password, security_answer):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "password": hash_password(password),
        "security_answer": hash_password(security_answer.lower().strip())
    }
    save_users(users)
    return True

def authenticate(username, password):
    users = load_users()
    if username not in users:
        return False
    return users[username]["password"] == hash_password(password)

def verify_security_answer(username, answer):
    users = load_users()
    if username not in users:
        return False
    return users[username]["security_answer"] == hash_password(answer.lower().strip())

def reset_password(username, new_password):
    users = load_users()
    if username not in users:
        return False
    users[username]["password"] = hash_password(new_password)
    save_users(users)
    return True
