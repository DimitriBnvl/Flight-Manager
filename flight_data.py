class FlightData:
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date


def find_cheapest_flight(data, return_date) -> FlightData | None:
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
        return_date=return_date,
    )
