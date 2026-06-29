# Flight Tracker

Searches Google Flights for cheap round-trip deals across the next 6 months and sends a WhatsApp alert when a price drops below the threshold stored in a Google Sheet.

## How it works

1. Reads destination cities, IATA codes, and price thresholds from a Google Sheet (via Sheety).
2. For each destination, queries SerpAPI's Google Flights engine once per month for the next 6 months, using a 7-day round trip per window.
3. If the cheapest fare found is below the sheet threshold, it updates the sheet and sends a WhatsApp message via the Twilio sandbox.

## Setup

### 1. Install dependencies

```bash
python -m ensurepip
python -m pip install requests requests-cache python-dotenv serpapi twilio
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```
SERP_API_KEY=your_serpapi_key
SHEETY_ENDPOINT=https://api.sheety.co/.../flightTracker/prices
SHEETY_USERNAME=your_sheety_username
SHEETY_PASSWORD=your_sheety_password
DEPARTURE_CITY_CODE=EDI
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+14155238886
TWILIO_TO_PHONE_NUMBER=+your_number
```

### 3. Join the Twilio WhatsApp sandbox

Send `join <your-sandbox-keyword>` to **+14155238886** on WhatsApp. The keyword is shown in your Twilio Console under **Messaging → Try it out → Send a WhatsApp message**.

### 4. Set up the Google Sheet

The sheet needs three columns: `city`, `airports` (IATA code), and `cheapestFlight` (price threshold). Share it with Sheety to get the endpoint.

## Usage

```bash
python main.py
```

## APIs used

| Service | Purpose |
|---|---|
| [SerpAPI](https://serpapi.com) | Google Flights search |
| [Sheety](https://sheety.co) | Google Sheets REST API |
| [Twilio](https://twilio.com) | WhatsApp notifications |