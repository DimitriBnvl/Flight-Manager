from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import requests_cache

requests_cache.install_cache(
    "flight_cache",
    expire_after=3600,
    urls_expire_after={
        "api.sheety.co": requests_cache.DO_NOT_CACHE,
    }
)

if __name__ == "__main__":
    data_manager = DataManager()
    flight_search = FlightSearch()
    notification_manager = NotificationManager()

    for destination in data_manager.get_data()["prices"]:
        city = destination["city"]
        iata_code = destination["airports"]
        lowest_price = destination["cheapestFlight"]
        row_id = destination["id"]

        print(f"Searching flights to {city} ({iata_code})...")
        cheapest = flight_search.find_cheapest(iata_code)

        if cheapest.price == "N/A":
            print(f"  No flights found to {city}.")
            continue

        else:
            print(
                f"  Cheapest: €{cheapest.price} | {cheapest.origin_airport} → "
                f"{cheapest.destination_airport} | Out: {cheapest.out_date} | Return: {cheapest.return_date}"
            )

        if cheapest.price < lowest_price:
            print(f"  Lower price found! (€{cheapest.price} vs sheet €{lowest_price})")
            data_manager.update_lowest_price(row_id, cheapest.price, cheapest.out_date, cheapest.return_date)
            notification_manager.send_sms(city, cheapest)