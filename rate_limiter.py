# rate_limiter.py

import time
from collections import defaultdict

# =========================
# STORE REQUESTS
# =========================
request_log = defaultdict(list)

# =========================
# BLOCKED IPS
# =========================
blocked_ips = {}

# Store block reasons
blocked_reasons = {}

# =========================
# CONFIG
# =========================
LIMIT = 10        # max requests
WINDOW = 60       # seconds
BLOCK_TIME = 120  # seconds


# =========================
# RATE LIMIT CHECK
# =========================
def is_rate_limited(ip):

    current_time = time.time()

    # =========================
    # CHECK IF ALREADY BLOCKED
    # =========================
    if ip in blocked_ips:

        if current_time < blocked_ips[ip]:
            return True

        else:
            del blocked_ips[ip]
            blocked_reasons.pop(ip, None)

    # =========================
    # REMOVE OLD REQUESTS
    # =========================
    request_log[ip] = [
        t for t in request_log[ip]
        if current_time - t < WINDOW
    ]

    # =========================
    # ADD CURRENT REQUEST
    # =========================
    request_log[ip].append(current_time)

    # =========================
    # LIMIT EXCEEDED
    # =========================
    if len(request_log[ip]) > LIMIT:

        blocked_ips[ip] = current_time + BLOCK_TIME

        blocked_reasons[ip] = "Rate Limit Exceeded"

        return True

    return False


# =========================
# CHECK IF BLOCKED
# =========================
def is_blocked(ip):

    current_time = time.time()

    if ip in blocked_ips:

        if current_time < blocked_ips[ip]:
            return True

        else:
            del blocked_ips[ip]
            blocked_reasons.pop(ip, None)

    return False


# =========================
# GET BLOCK REASON
# =========================
def get_block_reason(ip):

    return blocked_reasons.get(ip, "Not Blocked")


# =========================
# MANUAL BLOCK IP
# =========================
def block_ip(ip, reason="Manual Block"):

    blocked_ips[ip] = time.time() + BLOCK_TIME

    blocked_reasons[ip] = reason