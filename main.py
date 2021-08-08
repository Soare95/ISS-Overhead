import request
from datetime import datetime
import smtplib
import time

MY_LAT = 44.940399
MY_LONG = 26.023821

MY_EMAIL = "YOUR_EMAIL"
PASSWORD = "EMAIL_PASSWORD"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LONG-5 < iss_longitude < MY_LONG+5 and MY_LAT-5 < iss_latitude < MY_LAT+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunrise_hour or time_now <= sunset_hour:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=120)
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs="so4re_95@yahoo.com", msg="Subject: ISS UP!\n\n"
                                                                                   "Go check the sky!")
        connection.close()
