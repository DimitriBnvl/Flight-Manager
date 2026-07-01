class FlightData:
    """Holds the details of a single flight option returned by the search."""

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(data, return_date) -> FlightData:
    """Parse a SerpAPI Google Flights response and return the cheapest option.

    Merges best_flights and other_flights, skips entries with no price field,
    and returns a FlightData with 'N/A' fields if no valid flights are found.
    return_date is passed in explicitly because it is not present in the response.
    """
    flights = data.get("best_flights", []) + data.get("other_flights", [])
    if not flights:
        return FlightData(
            price="N/A",
            origin_airport="N/A",
            destination_airport="N/A",
            out_date="N/A",
            return_date="N/A",
            stops="N/A",
        )

    cheapest = None
    for flight in flights:
        try:
            price = flight["price"]
        except KeyError:
            continue
        if cheapest is None or price < cheapest["price"]:
            cheapest = flight

    if cheapest is None:
        return FlightData(
            price="N/A",
            origin_airport="N/A",
            destination_airport="N/A",
            out_date="N/A",
            return_date="N/A",
            stops="N/A",
        )

    first_leg = cheapest["flights"][0]
    last_leg = cheapest["flights"][-1]

    stops = len(cheapest.get("layovers", []))

    return FlightData(
        price=cheapest["price"],
        origin_airport=first_leg["departure_airport"]["id"],
        destination_airport=last_leg["arrival_airport"]["id"],
        out_date=first_leg["departure_airport"]["time"].split(" ")[0],
        return_date=return_date,
        stops=stops,
    )