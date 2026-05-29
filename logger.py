from database import insert_log

def log_attack(ip, threat):
    insert_log(ip, threat)
