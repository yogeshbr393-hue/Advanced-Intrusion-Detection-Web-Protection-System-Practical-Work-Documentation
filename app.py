from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from flask_session import Session
import random
import time
from datetime import datetime
from fpdf import FPDF
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "sentinelshield"
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

attack_count = 0

world_attacks = [
    {"country": "Russia", "x": 80, "y": 120},
    {"country": "China", "x": 300, "y": 160},
    {"country": "USA", "x": 150, "y": 90},
    {"country": "India", "x": 420, "y": 220},
]

threat_logs = [
    {"ip": "192.168.1.1", "status": "SAFE", "country": "India"},
    {"ip": "45.33.21.10", "status": "BLOCKED", "country": "Russia"},
    {"ip": "172.16.0.5", "status": "SAFE", "country": "USA"},
]

chatbot_responses = {
    "hello": "Hello Admin. SentinelShield AI is active.",
    "attack": "Current attack traffic detected from multiple regions.",
    "status": "Firewall and IDS systems are active.",
    "help": "Commands: hello, attack, status"
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

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    global attack_count

    attack_count += random.randint(1, 10)

    packet_data = []

    for i in range(15):

        packet_data.append({

            "source": f"192.168.0.{random.randint(1,255)}",
            "destination": f"10.0.0.{random.randint(1,255)}",
            "protocol": random.choice(["TCP", "UDP", "HTTP"]),
            "status": random.choice(["SAFE", "ATTACK"])

        })

    ml_prediction = random.choice([
        "LOW RISK",
        "MEDIUM RISK",
        "HIGH RISK",
        "CRITICAL ATTACK"
    ])

    return render_template(
        "dashboard.html",
        attack_count=attack_count,
        threat_logs=threat_logs,
        packet_data=packet_data,
        ml_prediction=ml_prediction,
        world_attacks=world_attacks
    )


@app.route("/chatbot", methods=["POST"])
def chatbot():

    message = request.form.get("message").lower()

    response = chatbot_responses.get(
        message,
        "AI Assistant processing request..."
    )

    return jsonify({"response": response})


@app.route("/generate-report")
def generate_report():

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=16)

    pdf.cell(200, 10, txt="SentinelShield Security Report", ln=True)

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Total Attacks: {attack_count}", ln=True)

    pdf.cell(200, 10, txt=f"ML Prediction: ACTIVE", ln=True)

    report_name = "security_report.pdf"

    pdf.output(report_name)

    return send_file(report_name, as_attachment=True)


@app.route("/send-alert")
def send_alert():

    return "Email Alert Sent Successfully"


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
