from cryptography.fernet import Fernet

# Generate this key once and store it securely
def generate_key():
    return Fernet.generate_key()

# Save and load key securely in production
key = b'your_32_byte_key_here'  # Replace with your actual key
cipher = Fernet(key)

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(token):
    return cipher.decrypt(token.encode()).decode()
