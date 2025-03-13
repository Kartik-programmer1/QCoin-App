# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

# File to store lottery entries
ENTRIES_FILE = 'lottery_entries.json'

def load_entries():
    if os.path.exists(ENTRIES_FILE):
        with open(ENTRIES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_entry(name, email):
    entries = load_entries()
    
    # Check if email already exists
    for entry in entries:
        if entry['email'] == email:
            return False
    
    # Add new entry
    entry = {
        'name': name,
        'email': email,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ticket_number': random.randint(1000, 9999)
    }
    entries.append(entry)
    
    with open(ENTRIES_FILE, 'w') as f:
        json.dump(entries, f, indent=4)
    
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enroll', methods=['POST'])
def enroll():
    name = request.form.get('name')
    email = request.form.get('email')
    
    if not name or not email:
        flash('Please provide both name and email', 'error')
        return redirect(url_for('index'))
    
    if '@' not in email or '.' not in email:
        flash('Please provide a valid email address', 'error')
        return redirect(url_for('index'))
    
    if save_entry(name, email):
        flash('Successfully enrolled in the QCoin lottery!', 'success')
    else:
        flash('This email is already registered', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)