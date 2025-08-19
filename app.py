import pyotp
from flask import Flask, render_template, request, redirect, session
from utils.encryptor import encrypt_data, decrypt_data
import json

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Load users from Mockaroo
with open("users/fake_users.json") as f:
    users = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Mock login
        user = next((u for u in users if u['email'] == email), None)
        if user and user['password'] == password:
            session['user'] = user['email']
            session['otp_secret'] = pyotp.random_base32()
            totp = pyotp.TOTP(session['otp_secret'])
            print(f"Secret: {session['otp_secret']} | OTP: {totp.now()}")
            return redirect('/2fa')
    return render_template('login.html')

@app.route('/2fa', methods=['GET', 'POST'])
def two_factor():
    if request.method == 'POST':
        user_input_otp = request.form['otp']
        totp = pyotp.TOTP(session['otp_secret'])
        if totp.verify(user_input_otp):
            return redirect('/dashboard')
    return render_template('2fa.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    encrypted = encrypt_data("Sensitive Info")
    decrypted = decrypt_data(encrypted)
    return render_template('dashboard.html', email=session['user'], encrypted=encrypted, decrypted=decrypted)

if __name__ == '__main__':
    app.run(debug=True)
