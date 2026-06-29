import requests
from dotenv import load_dotenv
import os

load_dotenv()


class DataManager:
    """Handles all reads and writes to the Google Sheet via the Sheety REST API."""
    def __init__(self):
        self.sheety_endpoint = os.environ["SHEETY_ENDPOINT"]
        self.auth = (os.environ["SHEETY_USERNAME"], os.environ["SHEETY_PASSWORD"])

        response = requests.get(self.sheety_endpoint, auth=self.auth)
        self._data = response.json()

    def get_data(self):
        """Return the sheet data fetched at initialisation."""
        return self._data

    def update_lowest_price(self, row_id, new_price):
        """Overwrite the cheapestFlight value for a given row in the sheet."""
        requests.put(
            f"{self.sheety_endpoint}/{row_id}",
            json={"price": {"cheapestFlight": new_price}},
            auth=self.auth,
        )