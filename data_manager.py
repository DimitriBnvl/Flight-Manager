import requests
from dotenv import load_dotenv
import os
load_dotenv()

class DataManager:
    def __init__(self):
        self.sheety_endpoint = os.environ["SHEETY_ENDPOINT"]
        self.response = requests.get(
            self.sheety_endpoint,
            auth=(os.environ["SHEETY_USERNAME"], os.environ["SHEETY_PASSWORD"])
        )

    def get_data(self):
        return self.response.json()
