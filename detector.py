import re

# Attack detection patterns
patterns = {

    "SQL Injection": [
        r"(?i)(union\s+select)",
        r"(?i)(or\s+1=1)",
        r"(?i)(drop\s+table)",
        r"(?i)(delete\s+from)"
    ],

    "XSS": [
        r"(?i)<script>",
        r"(?i)javascript:",
        r"(?i)onerror="
    ],

    "Directory Traversal": [
        r"\.\./",
        r"\.\.\\"
    ],

    "Command Injection": [
        r"(?i)(;\s*ls)",
        r"(?i)(;\s*cat)",
        r"(?i)(&&)",
        r"(?i)(\|\|)"
    ],

    "Local File Inclusion": [
        r"/etc/passwd",
        r"boot.ini"
    ]
}

# Attack detection function
def detect_attack(data):

    # Convert data to string
    data = str(data)

    # Check every attack pattern
    for attack, regex_list in patterns.items():

        for pattern in regex_list:

            if re.search(pattern, data):

                return attack

    # No attack found
    return None