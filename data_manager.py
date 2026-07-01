import requests
from dotenv import load_dotenv
import os

load_dotenv()


class DataManager:
    """Handles all reads and writes to the Google Sheet via the Sheety REST API."""
    def __init__(self):
        self.prices_endpoint = os.environ["SHEETY_PRICES_ENDPOINT"]
        self.users_endpoint  = os.environ["SHEETY_USERS_ENDPOINT"]
        self.auth            = (os.environ["SHEETY_USERNAME"], os.environ["SHEETY_PASSWORD"])

        response = requests.get(self.prices_endpoint, auth=self.auth)
        self._data = response.json()

    def get_data(self):
        """Return the sheet data fetched at initialisation."""
        return self._data

    def update_lowest_price(self, row_id, new_price, departure_date, arrival_date, stops):
        """Overwrite cheapestFlight, departureDate, arrivalDate, and stops for a given row."""
        response = requests.put(
            f"{self.prices_endpoint}/{row_id}",
            json={"price": {
                "cheapestFlight": new_price,
                "departureDate": departure_date,
                "arrivalDate": arrival_date,
                "stops": stops,
            }},
            auth=self.auth,
        )
        print(f"  Sheety PUT status: {response.status_code}")

    def get_customer_emails(self):
        response2 = requests.get(self.users_endpoint, auth=self.auth)
        return response2.json()
