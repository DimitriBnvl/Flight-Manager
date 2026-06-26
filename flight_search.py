import os
import serpapi
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight, FlightData

load_dotenv()

TRIP_DURATION_DAYS = 7
SEARCH_STEP_DAYS = 28  # check one departure date per month


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

    def find_cheapest(self, arrival_id) -> FlightData:
        cheapest = None
        outbound = self.tomorrow

        while outbound <= self.six_months_from_now - timedelta(days=TRIP_DURATION_DAYS):
            return_dt = outbound + timedelta(days=TRIP_DURATION_DAYS)
            data = self._get_flights(arrival_id, outbound, return_dt)
            flight = find_cheapest_flight(data, return_dt.strftime("%Y-%m-%d"))

            if flight.price != "N/A":
                if cheapest is None or flight.price < cheapest.price:
                    cheapest = flight

            outbound += timedelta(days=SEARCH_STEP_DAYS)

        return cheapest or FlightData(
            price="N/A",
            origin_airport="N/A",
            destination_airport="N/A",
            out_date="N/A",
            return_date="N/A",
        )

    def _get_flights(self, arrival_id, outbound_date, return_date):
        return self.client.search({
            "engine": "google_flights",
            "departure_id": self.departure_city_code,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date.strftime("%Y-%m-%d"),
            "return_date": return_date.strftime("%Y-%m-%d"),
            "type": self.type,
            "travel_class": self.travel_class,
            "adults": self.adults,
            "currency": self.currency,
            "stops": self.stops,
        })