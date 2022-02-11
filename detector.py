import requests
from datetime import datetime
from dotenv import dotenv_values

from notifier import send_email
from utils import datetime_from_utc_to_local

config = dotenv_values(".env")

MY_LAT = float(config["MY_LAT"])
MY_LONG = float(config["MY_LONG"])
EMAIL = config["EMAIL"]
PASSWORD = config["PASSWORD"]
RECIPIENT = config["RECIPIENT"]


def get_iss_position():
    """Returns a tuple of ISS's lat and long e.g.(23.259933, 77.412613)"""
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_lat = float(data["iss_position"]["latitude"])
    iss_lng = float(data["iss_position"]["longitude"])

    return iss_lat, iss_lng


def get_twilight_hours(params):
    """Returns a tuple of sunrise and sunset hours in UTC e.g. (06, 19)"""
    response = requests.get("https://api.sunrise-sunset.org/json", params=params)
    response.raise_for_status()
    data = response.json()
    sunrise = datetime_from_utc_to_local(data["results"]["sunrise"])[0]
    sunset = datetime_from_utc_to_local(data["results"]["sunset"])[0]
    return sunrise, sunset


def is_currently_dark():
    sunrise_hour, sunset_hour = get_twilight_hours(params={
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    })
    now = datetime.now()
    now_hour = now.strftime("%H")

    if now_hour < sunrise_hour or now_hour > sunset_hour:
        return True

    return False


def is_iss_overhead():
    iss_lat, iss_lng = get_iss_position()
    return abs(iss_lat - MY_LAT) <= 5 and abs(iss_lng - MY_LONG) <= 5


def detect_iss():
    print("Scanning for ISS... 🔭")
    if is_iss_overhead() and is_currently_dark():
        print("ISS Detected nearby! 🛰")
        send_email(
            EMAIL,
            PASSWORD,
            RECIPIENT
        )
        print("Email notification sent! 📧")
