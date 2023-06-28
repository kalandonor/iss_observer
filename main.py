import requests
from datetime import datetime

MY_LAT = 51.480301741130134
MY_LNG = 5.432284326071018
SUNRISE_SUNSET_ENDPOINT = "https://api.sunrise-sunset.org/json"
ISS_API_ENDPOINT = "http://api.open-notify.org/iss-now.json"


def get_current_hour():
    now = datetime.now()
    return now.hour


def get_iss_position():
    iss_response = requests.get(ISS_API_ENDPOINT)
    iss_response.raise_for_status()
    iss_lat = iss_response.json()["iss_position"]["latitude"]
    iss_lon = iss_response.json()["iss_position"]["longitude"]
    return float(iss_lat), float(iss_lon)


class IssObserver:
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.lon = longitude
        self.sunrise_sunset_dict = self.get_sunrise_sunset()
        self.now_hour = get_current_hour()

    def get_sunrise_sunset(self):
        parameters = {
            "lat": self.lat,
            "lng": self.lon,
            "formatted": 0,
        }
        response = requests.get(SUNRISE_SUNSET_ENDPOINT, params=parameters)
        response.raise_for_status()
        sunset = response.json()['results']['sunset']
        sunrise = response.json()['results']['sunrise']
        sunset_hours = int(sunset.split("T")[1].split(":")[0]) + 2
        sunrise_hours = int(sunrise.split("T")[1].split(":")[0]) + 2
        return {"sunrise": sunrise_hours, "sunset": sunset_hours}

    def observe_iss(self):
        if not self.is_it_night():
            print("ISS isn't observable during daytime.")
        else:
            if self.check_iss_is_in_good_position():
                print("ISS is visible! Go out and look up!")
            else:
                print("ISS isn't visible!")

    def is_it_night(self):
        if self.now_hour <= self.sunrise_sunset_dict.get("sunrise") or \
                self.now_hour >= self.sunrise_sunset_dict.get("sunset"):
            return True
        else:
            return False

    def check_iss_is_in_good_position(self):
        iss_lat, iss_lon = get_iss_position()
        return iss_lat - 5 < self.lat < iss_lat + 5 and iss_lon - 5 < self.lon < iss_lon + 5


if __name__ == "__main__":
    observer = IssObserver(MY_LAT, MY_LNG)
    observer.observe_iss()
