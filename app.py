from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import sqlite3
import os
import random
import time

app = Flask(__name__)

# =========================
# SESSION CONFIG
# =========================

app.config["SECRET_KEY"] = "sentinelshield_secret_key"
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# =========================
# LOGIN CREDENTIALS
# =========================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# =========================
# DATABASE CREATE
# =========================

def create_database():

    conn = sqlite3.connect("sentinelshield.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        status TEXT,
        country TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()

create_database()

# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():
    return redirect('/login')

# =========================
# LOGIN PAGE
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session['user'] = username

            return redirect('/dashboard')

        else:
            return """
            <h2>Invalid Username or Password</h2>
            <a href='/login'>Try Again</a>
            """

    return """

    <html>

    <head>

    <title>SentinelShield Login</title>

    <style>

    body{
        background:#07172a;
        color:white;
        font-family:Arial;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
    }

    .box{
        background:#16253d;
        padding:40px;
        border-radius:10px;
        width:300px;
    }

    input{
        width:100%;
        padding:10px;
        margin-top:10px;
        border:none;
        border-radius:5px;
    }

    button{
        width:100%;
        padding:10px;
        margin-top:20px;
        background:#38bdf8;
        border:none;
        color:black;
        font-weight:bold;
        border-radius:5px;
    }

    h1{
        color:#38bdf8;
    }

    </style>

    </head>

    <body>

        <div class="box">

            <h1>SentinelShield</h1>

            <form method="POST">

                <input type="text" name="username" placeholder="Username" required>

                <input type="password" name="password" placeholder="Password" required>

                <button type="submit">Login</button>

            </form>

        </div>

    </body>

    </html>

    """

# =========================
# DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    ai_alerts = [
        "AI engine reports system operating normally",
        "Firewall active and protecting server",
        "No SQL injection detected",
        "Threat monitoring enabled",
        "Intrusion Detection System Online"
    ]

    logs = [

        {
            "ip":"192.168.1.1",
            "status":"SAFE",
            "country":"India"
        },

        {
            "ip":"45.33.21.10",
            "status":"BLOCKED",
            "country":"Russia"
        },

        {
            "ip":"172.16.0.5",
            "status":"SAFE",
            "country":"USA"
        }

    ]

    return render_template(
        'dashboard.html',
        ai_alerts=ai_alerts,
        logs=logs
    )

# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

# =========================
# RUN APP
# =========================

if __name__ == '__main__':
    app.run(debug=True)
