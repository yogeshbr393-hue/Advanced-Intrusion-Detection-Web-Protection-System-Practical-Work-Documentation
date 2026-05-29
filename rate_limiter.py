from time import time

requests_log = {}

LIMIT = 10
WINDOW = 60

def is_rate_limited(ip):
    current_time = time()

    if ip not in requests_log:
        requests_log[ip] = []

    requests_log[ip] = [
        t for t in requests_log[ip]
        if current_time - t < WINDOW
    ]

    requests_log[ip].append(current_time)

    return len(requests_log[ip]) > LIMIT
