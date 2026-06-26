from data_manager import DataManager
from flight_search import FlightSearch
import requests_cache

requests_cache.install_cache(
    "flight_cache",
    expire_after=3600,
    urls_expire_after={
        "api.sheety.co": requests_cache.DO_NOT_CACHE,
    }
)

if __name__ == "__main__":
    sheet_data = DataManager()
    flight_search = FlightSearch()

    flight_search.check_flights(sheet_data)