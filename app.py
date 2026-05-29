from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
import random
import time
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "sentinelshield"
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

attack_count = 0

threat_logs = [
    {"ip": "192.168.1.1", "status": "SAFE", "country": "India"},
    {"ip": "45.33.21.10", "status": "BLOCKED", "country": "Russia"},
    {"ip": "172.16.0.5", "status": "SAFE", "country": "USA"},
]

chatbot_responses = {
    "hello": "Hello Admin. SentinelShield AI is active.",
    "attack": "No critical attacks detected currently.",
    "status": "Firewall and IDS systems are active.",
    "help": "Available commands: hello, attack, status"
}


@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["user"] = username
            return redirect("/dashboard")

        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    global attack_count

    attack_count += random.randint(1, 5)

    packet_data = []

    for i in range(10):
        packet_data.append({
            "source": f"192.168.0.{random.randint(1,255)}",
            "destination": f"10.0.0.{random.randint(1,255)}",
            "protocol": random.choice(["TCP", "UDP", "HTTP"]),
            "status": random.choice(["SAFE", "SUSPICIOUS"])
        })

    ml_prediction = random.choice([
        "Low Threat",
        "Medium Threat",
        "High Threat"
    ])

    return render_template(
        "dashboard.html",
        attack_count=attack_count,
        threat_logs=threat_logs,
        packet_data=packet_data,
        ml_prediction=ml_prediction,
        current_time=datetime.now()
    )


@app.route("/chatbot", methods=["POST"])
def chatbot():

    message = request.form.get("message").lower()

    response = chatbot_responses.get(
        message,
        "AI Assistant could not understand the command."
    )

    return jsonify({"response": response})


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
