from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_session import Session
import sqlite3
import requests

from detector import detect_attack
from logger import log_attack
from database import create_tables, insert_attack
from rate_limiter import is_rate_limited
from blacklist import is_blocked, block_ip

app = Flask(__name__)

# =========================
# SESSION CONFIG
# =========================
app.config["SECRET_KEY"] = "sentinelshield_secret_key"
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# =========================
# CREATE DATABASE
# =========================
create_tables()

# =========================
# LOGIN CREDENTIALS
# =========================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# =========================
# GEO IP TRACKING
# =========================
def get_geo_location(ip):

    try:

        response = requests.get(
            f"http://ip-api.com/json/{ip}"
        )

        data = response.json()

        city = data.get("city", "Unknown")
        country = data.get("country", "Unknown")

        return f"{city}, {country}"

    except:
        return "Unknown Location"


# =========================
# HOME ROUTE
# =========================
@app.route("/")
def home():

    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>SentinelShield</title>

        <style>

            body{
                background:#050b18;
                color:white;
                font-family:Arial;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }

            .box{
                text-align:center;
                background:#111827;
                padding:50px;
                border-radius:15px;
                width:500px;
                box-shadow:0 0 25px rgba(0,0,0,0.5);
            }

            h1{
                color:#38bdf8;
                font-size:42px;
            }

            p{
                color:#cbd5e1;
                margin-top:15px;
                font-size:18px;
            }

            button{
                margin-top:30px;
                padding:14px 30px;
                background:#38bdf8;
                border:none;
                border-radius:10px;
                color:white;
                font-size:18px;
                cursor:pointer;
            }

            button:hover{
                background:#0ea5e9;
            }

        </style>

    </head>

    <body>

        <div class="box">

            <h1>🛡 SentinelShield</h1>

            <p>
                Advanced Intrusion Detection & Threat Monitoring System
            </p>

            <a href='/login'>
                <button>
                    Open Admin Dashboard
                </button>
            </a>

        </div>

    </body>

    </html>
    """


# =========================
# LOGIN ROUTE
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect(url_for("dashboard"))

        return """
        <h2 style='color:red;text-align:center;margin-top:50px;'>
            Invalid Credentials
        </h2>

        <div style='text-align:center;'>
            <a href='/login'>Try Again</a>
        </div>
        """

    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>SentinelShield Login</title>

        <style>

            body{
                background:#050b18;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
                font-family:Arial;
                color:white;
            }

            .login-box{
                background:#111827;
                padding:40px;
                border-radius:15px;
                width:350px;
                box-shadow:0 0 25px rgba(0,0,0,0.6);
            }

            h1{
                text-align:center;
                color:#38bdf8;
            }

            input{
                width:100%;
                padding:14px;
                margin-top:15px;
                border:none;
                border-radius:8px;
                font-size:16px;
                background:#1e293b;
                color:white;
            }

            button{
                width:100%;
                padding:14px;
                margin-top:20px;
                background:#38bdf8;
                border:none;
                border-radius:8px;
                font-size:18px;
                cursor:pointer;
                color:white;
            }

            button:hover{
                background:#0ea5e9;
            }

        </style>

    </head>

    <body>

        <div class="login-box">

            <h1>🛡 SentinelShield</h1>

            <form method="POST">

                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    required
                >

                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    required
                >

                <button type="submit">
                    Login
                </button>

            </form>

        </div>

    </body>

    </html>
    """


# =========================
# LOGOUT ROUTE
# =========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================
# TEST ROUTE
# =========================
@app.route("/test")
def test():

    data = str(request.args)

    ip = request.remote_addr

    location = get_geo_location(ip)

    # =========================
    # BLACKLIST CHECK
    # =========================
    if is_blocked(ip):

        log_attack(ip, "Blacklisted", data)
        insert_attack("Blacklisted", data, ip)

        return jsonify({
            "status": "blocked",
            "reason": "IP Blacklisted",
            "location": location
        })

    # =========================
    # RATE LIMIT CHECK
    # =========================
    if is_rate_limited(ip):

        log_attack(ip, "Rate Limited", data)
        insert_attack("Rate Limited", data, ip)

        block_ip(ip)

        return jsonify({
            "status": "blocked",
            "reason": "Rate limit exceeded",
            "location": location
        })

    # =========================
    # ATTACK DETECTION
    # =========================
    attack = detect_attack(data)

    if attack:

        log_attack(ip, attack, data)
        insert_attack(attack, data, ip)

        if attack in ["SQL Injection", "XSS"]:
            block_ip(ip)

        return jsonify({
            "status": "blocked",
            "attack": attack,
            "location": location
        })

    # =========================
    # SAFE TRAFFIC
    # =========================
    log_attack(ip, "Safe", data)
    insert_attack("Safe", data, ip)

    return jsonify({
        "status": "safe",
        "location": location
    })


# =========================
# DASHBOARD ROUTE
# =========================
@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = sqlite3.connect("database/sentinel.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM attack_logs
        ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    # =========================
    # COUNTS
    # =========================
    cursor.execute("SELECT COUNT(*) FROM attack_logs")
    total_attacks = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM attack_logs
        WHERE attack_type='SQL Injection'
    """)
    sqli_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM attack_logs
        WHERE attack_type='XSS'
    """)
    xss_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM attack_logs
        WHERE attack_type='Blacklisted'
    """)
    blacklist_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM attack_logs
        WHERE attack_type='Rate Limited'
    """)
    rate_limit_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM attack_logs
        WHERE attack_type='Safe'
    """)
    safe_count = cursor.fetchone()[0]

    # =========================
    # THREAT SEVERITY
    # =========================
    total_threats = (
        sqli_count +
        xss_count +
        blacklist_count +
        rate_limit_count
    )

    if total_threats >= 10:
        severity = "CRITICAL RISK"
        severity_color = "#ef4444"

    elif total_threats >= 5:
        severity = "HIGH RISK"
        severity_color = "#f97316"

    elif total_threats >= 2:
        severity = "MEDIUM RISK"
        severity_color = "#facc15"

    else:
        severity = "LOW RISK"
        severity_color = "#22c55e"

    # =========================
    # AI ALERTS
    # =========================
    ai_alerts = []

    if sqli_count >= 5:
        ai_alerts.append(
            "⚠ AI detected abnormal SQL Injection spike"
        )

    if xss_count >= 2:
        ai_alerts.append(
            "⚠ AI detected repeated XSS attack attempts"
        )

    if blacklist_count >= 2:
        ai_alerts.append(
            "🚨 Multiple blacklisted IPs attempted access"
        )

    if rate_limit_count >= 3:
        ai_alerts.append(
            "⚠ Suspicious traffic flooding detected"
        )

    if total_threats >= 8:
        ai_alerts.append(
            "🚨 AI anomaly engine predicts coordinated attack activity"
        )

    if len(ai_alerts) == 0:
        ai_alerts.append(
            "✅ AI engine reports system operating normally"
        )

    conn.close()

    return render_template(

        "dashboard.html",

        logs=logs,

        total_attacks=total_attacks,

        sqli_count=sqli_count,

        xss_count=xss_count,

        blacklist_count=blacklist_count,

        rate_limit_count=rate_limit_count,

        safe_count=safe_count,

        severity=severity,

        severity_color=severity_color,

        ai_alerts=ai_alerts
    )


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":

    app.run(debug=True)
