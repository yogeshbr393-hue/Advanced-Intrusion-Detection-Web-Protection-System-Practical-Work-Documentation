from datetime import datetime
from database import insert_attack

# Log file path
LOG_FILE = "logs/attacks.log"

# Logging function
def log_attack(ip, attack_type, payload):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"{timestamp} | "
        f"IP: {ip} | "
        f"Attack: {attack_type} | "
        f"Payload: {payload}\n"
    )

    # Save to log file
    with open(LOG_FILE, "a") as file:

        file.write(log_entry)

    # Save to SQLite database
    insert_attack(attack_type, payload, ip)