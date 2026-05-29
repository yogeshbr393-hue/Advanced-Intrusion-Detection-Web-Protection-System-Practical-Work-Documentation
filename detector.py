def detect_attack(user_input):
    suspicious_keywords = [
        "script",
        "drop table",
        "select *",
        "union",
        "--",
        "<script>"
    ]

    for keyword in suspicious_keywords:
        if keyword.lower() in user_input.lower():
            return True

    return False
