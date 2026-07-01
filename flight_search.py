import os
import serpapi
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight, FlightData

load_dotenv()

TRIP_DURATION_DAYS = 7
SEARCH_STEP_DAYS = 28  # check one departure date per month


class FlightSearch:
    """Queries the SerpAPI Google Flights engine to find cheap round-trip fares."""
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
        """Search monthly across the next 6 months and return the cheapest 7-day round trip."""
        cheapest = None
        outbound_date = self.tomorrow

        while outbound_date <= self.six_months_from_now - timedelta(days=TRIP_DURATION_DAYS):
            return_date = outbound_date + timedelta(days=TRIP_DURATION_DAYS)
            data = self._get_flights(arrival_id, outbound_date, return_date)
            flight = find_cheapest_flight(data, return_date.strftime("%Y-%m-%d"))

            if flight.price != "N/A":
                if cheapest is None or flight.price < cheapest.price:
                    cheapest = flight

            outbound_date += timedelta(days=SEARCH_STEP_DAYS)

        return cheapest or FlightData(
            price="N/A",
            origin_airport="N/A",
            destination_airport="N/A",
            out_date="N/A",
            return_date="N/A",
            stops="N/A",
        )

    def _get_flights(self, arrival_id, outbound_date, return_date):
        """Make a single SerpAPI call for the given arrival airport and date pair."""
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