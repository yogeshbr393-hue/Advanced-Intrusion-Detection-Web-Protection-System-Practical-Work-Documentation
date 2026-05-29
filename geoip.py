import requests

def get_geo_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()

        return {
            "country": data.get("country"),
            "city": data.get("city"),
            "isp": data.get("isp")
        }

    except:
        return {
            "country": "Unknown",
            "city": "Unknown",
            "isp": "Unknown"
        }
