import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 43.651890
MY_LONG = -79.381706
MY_EMAIL = "youremail@gmail.com"
PASSWORD = ""


def iss_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= -MY_LONG + 5:
        return True


def night_time():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = (int(data["results"]["sunrise"].split("T")[1].split(":")[0])) - 4
    sunset = (int(data["results"]["sunset"].split("T")[1].split(":")[0])) - 4

    time_now = datetime.now().hour

    if sunset <= time_now or time_now <= sunrise:
        return True


#If the ISS is close to my current position

while night_time():
    time.sleep(60)
    if iss_near():
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user= MY_EMAIL, password = PASSWORD)
            connection.sendmail(to_addrs="youremail@gmail.com",
                                from_addr= MY_EMAIL,
                                msg= "Subject: ISS Above You \n\n Look up! "
                                )




