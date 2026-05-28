import requests


def get_ip_info(ip):

    try:

        response = requests.get(
            f"http://ip-api.com/json/{ip}"
        )

        data = response.json()

        return {
            "country": data.get("country", "Unknown"),
            "city": data.get("city", "Unknown"),
            "isp": data.get("isp", "Unknown")
        }

    except:
        return {
            "country": "Unknown",
            "city": "Unknown",
            "isp": "Unknown"
        }
