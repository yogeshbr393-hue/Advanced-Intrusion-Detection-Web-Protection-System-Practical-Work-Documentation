# blacklist.py

import datetime

# =========================
# IN-MEMORY BLACKLIST STORAGE
# =========================

# Stores blocked IP addresses
blocked_ips = set()

# Stores blacklist history/logs
blacklist_log = []


# =========================
# BLOCK IP FUNCTION
# =========================
def block_ip(ip, reason="Auto Block"):

    # Add IP to blocked list
    blocked_ips.add(ip)

    # Save log entry
    blacklist_log.append({
        "ip": ip,
        "reason": reason,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


# =========================
# CHECK IF IP IS BLOCKED
# =========================
def is_blocked(ip):

    return ip in blocked_ips


# =========================
# GET BLACKLIST LOGS
# =========================
def get_blacklist_logs():

    return blacklist_log


# =========================
# OPTIONAL: UNBLOCK IP
# =========================
def unblock_ip(ip):

    if ip in blocked_ips:
        blocked_ips.remove(ip)


# =========================
# OPTIONAL: CLEAR ALL BLOCKED IPS
# =========================
def clear_blacklist():

    blocked_ips.clear()