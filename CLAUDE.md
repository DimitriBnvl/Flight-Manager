# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the project

```bash
python main.py
```

Dependencies are managed via a `.venv`. Install packages with:

```bash
python -m ensurepip && python -m pip install <package>
```

Required packages: `requests`, `requests-cache`, `python-dotenv`, `serpapi`, `twilio`.

## Environment variables

All secrets live in `.env`. Required keys:

| Variable                                   | Purpose                                   |
|--------------------------------------------|-------------------------------------------|
| `SERP_API_KEY`                             | SerpAPI key for Google Flights queries    |
| `SHEETY_ENDPOINT`                          | Sheety REST endpoint for the Google Sheet |
| `SHEETY_USERNAME` / `SHEETY_PASSWORD`      | Sheety basic auth                         |
| `DEPARTURE_CITY_CODE`                      | IATA code of the origin airport           |
| `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` | Twilio credentials                        |
| `TWILIO_PHONE_NUMBER`                      | Twilio WhatsApp sandbox sender            |
| `TWILIO_TO_PHONE_NUMBER`                   | Recipient phone number in E.164 format    |

## Architecture

The program has four classes, each in its own file, plus a top-level orchestrator:

**`main.py`** — orchestrates the full loop: fetch sheet → search flights → compare price → update sheet → notify.

**`DataManager`** (`data_manager.py`) — talks to Sheety (a Google Sheets REST wrapper). `get_data()` returns the cached JSON fetched at init. `update_lowest_price(row_id, price)` PUTs a new `cheapestFlight` value back to the sheet. Sheety's JSON key for a row update must match the singular form of the sheet tab name (`"price": {...}`).

**`FlightSearch`** (`flight_search.py`) — wraps the SerpAPI Google Flights engine. `find_cheapest(arrival_id)` loops through ~6 departure dates (monthly steps, `SEARCH_STEP_DAYS = 28`) across the next 6 months, each paired with a 7-day return (`TRIP_DURATION_DAYS = 7`), and returns the single cheapest `FlightData` found. The inner `_get_flights()` makes one SerpAPI call per date pair.

**`FlightData`** + `find_cheapest_flight()` (`flight_data.py`) — `FlightData` is a plain data container. `find_cheapest_flight(data, return_date)` parses a raw SerpAPI response: it merges `best_flights` and `other_flights`, skips entries missing a `price` key, and returns a `FlightData` with `"N/A"` fields when no results exist.

**`NotificationManager`** (`notification_manager.py`) — sends a WhatsApp message via the Twilio sandbox using `whatsapp:` prefixed numbers. The recipient must have joined the sandbox before messages can be delivered.

## Caching

`requests-cache` is installed globally in `main.py` with a 1-hour TTL. Sheety calls are excluded (`DO_NOT_CACHE`) so sheet reads are always fresh. SerpAPI calls are cached, so re-running within an hour won't burn API quota.