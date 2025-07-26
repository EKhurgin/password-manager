#
#  password_manager.py
#
#
#  Created by Eli Khurgin on 7/25/25.
#
import getpass
import json
from cryptography.fernet import Fernet
import os

PASSWORDS_FILE = "passwords.json"
KEY_FILE = "secret.key"

# Generate a key and save it, or load it if it already exists
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

key = load_key()
fernet = Fernet(key)

def load_passwords():
    if not os.path.exists(PASSWORDS_FILE):
        return {}
    with open(PASSWORDS_FILE, "rb") as f:
        encrypted_data = f.read()
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except Exception as e:
        print("Error decrypting data:", e)
        return {}

def save_passwords(passwords):
    data = json.dumps(passwords).encode()
    encrypted_data = fernet.encrypt(data)
    with open(PASSWORDS_FILE, "wb") as f:
        f.write(encrypted_data)

def add_password(account, password):
    passwords = load_passwords()
    passwords[account] = password
    save_passwords(passwords)

def get_password(account):
    passwords = load_passwords()
    return passwords.get(account, None)

def main():
    while True:
        choice = input("Choose: [1] Add password [2] Get password [3] Exit: ").strip()
        if choice == "1":
            acc = input("Account name: ").strip()
            pw = getpass.getpass("Password: ")
            add_password(acc, pw)
            print("Saved!")
        elif choice == "2":
            acc = input("Account name: ").strip()
            pw = get_password(acc)
            if pw:
                print(f"Password: {pw}")
            else:
                print("Not found.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
