import os
import serpapi
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flight_data import FlightData

load_dotenv()

class FlightSearch:
    def __init__(self):
        self.type         = "1" #1 = One Way, 2 = Round Trip, 3 = Multi City
        self.adults       = "1"
        self.travel_class = "1" # 1 = Economy, 2 = Economy Premium, 3 = Business Class, 4 = First Class
        self.currency     = "EUR"
        self.stops        = "0" # 0 = Any, 1 = Nonstop, 2 = 1 stop or fewer

        self.departure_city_code = os.environ["DEPARTURE_CITY_CODE"]
        self.api_key             = os.environ["SERP_API_KEY"]

        self.tomorrow_date       = datetime.now() + timedelta(days=1)
        self.six_months_from_now = datetime.now() + timedelta(days=180)

        self.client = serpapi.Client(api_key=self.api_key)

    def check_flights(self, sheet_data):
        for destination in sheet_data.get_data()["prices"]:
            iata_code = destination["airports"]
            print(f"Searching flights to {destination['city']} ({iata_code})...")
            data = self.get_flights(iata_code)
            cheapest = self.find_cheapest_flight(data)
            if cheapest:
                print(f"  Cheapest: €{cheapest.price} | {cheapest.origin_airport} → {cheapest.destination_airport} on {cheapest.out_date}")

    def find_cheapest_flight(self, data):
        flights = data.get("best_flights", []) + data.get("other_flights", [])
        if not flights:
            return None
        cheapest = min(flights, key=lambda x: x["price"])
        first_leg = cheapest["flights"][0]
        last_leg  = cheapest["flights"][-1]
        return FlightData(
            price=cheapest["price"],
            origin_airport=first_leg["departure_airport"]["id"],
            destination_airport=last_leg["arrival_airport"]["id"],
            out_date=first_leg["departure_airport"]["time"].split(" ")[0],
            return_date=self.six_months_from_now.strftime("%Y-%m-%d"),
        )

    def get_flights(self, arrival_id):
        return self.client.search({
            "engine": "google_flights",
            "departure_id": self.departure_city_code,
            "arrival_id": arrival_id,
            "outbound_date": self.tomorrow_date.strftime("%Y-%m-%d"),
            "return_date": self.six_months_from_now.strftime("%Y-%m-%d"),
            "type": self.type,
            "travel_class": self.travel_class,
            "adults": self.adults,
            "currency": self.currency,
            "stops": self.stops,
        })