blacklisted_ips = set()

def add_to_blacklist(ip):
    blacklisted_ips.add(ip)

def is_blacklisted(ip):
    return ip in blacklisted_ips
