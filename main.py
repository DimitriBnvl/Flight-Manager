#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from pprint import pprint
import requests_cache
from datetime import datetime, timedelta

requests_cache.install_cache(
    "flight_cache",
    expire_after=3600,
    urls_expire_after={
        "api.sheety.co": requests_cache.DO_NOT_CACHE,
    }
)

if __name__ == "__main__":
    tomorrow = datetime.now() + timedelta(days=1)
    six_months = datetime.now() + timedelta(days=180)

    sheet_data = DataManager()
    pprint(sheet_data.get_data())