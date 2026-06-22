#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from pprint import pprint
import requests_cache
from requests_cache import DO_NOT_CACHE, NEVER_EXPIRE, CachedSession
from datetime import datetime, timedelta

requests_cache.install_cache()

if __name__ == "__main__":
    tomorrow = datetime.now() + timedelta(days=1)
    six_months = datetime.now() + timedelta(days=180)

    urls_expire_after = {
        'https://api.sheety.co/': DO_NOT_CACHE,
        '*': 3600,
    }
    session = CachedSession(urls_expire_after=urls_expire_after)

    sheet_data = DataManager()
    pprint(sheet_data.get_data())