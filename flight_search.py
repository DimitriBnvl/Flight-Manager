import os
import serpapi
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()


class FlightSearch:
    def __init__(self):
        self.type = "1"          # 1 = Round Trip
        self.adults = "1"
        self.travel_class = "1"  # 1 = Economy
        self.currency = "EUR"
        self.stops = "0"         # 0 = Any

        self.departure_city_code = os.environ["DEPARTURE_CITY_CODE"]
        self.api_key = os.environ["SERP_API_KEY"]

        self.tomorrow = datetime.now() + timedelta(days=1)
        self.six_months_from_now = datetime.now() + timedelta(days=180)

        self.client = serpapi.Client(api_key=self.api_key)

    def get_flights(self, arrival_id):
        return self.client.search({
            "engine": "google_flights",
            "departure_id": self.departure_city_code,
            "arrival_id": arrival_id,
            "outbound_date": self.tomorrow.strftime("%Y-%m-%d"),
            "return_date": self.six_months_from_now.strftime("%Y-%m-%d"),
            "type": self.type,
            "travel_class": self.travel_class,
            "adults": self.adults,
            "currency": self.currency,
            "stops": self.stops,
        })