import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:
    """Sends flight deal alerts via WhatsApp using the Twilio sandbox."""
    def __init__(self):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"],
        )
        self.from_number = os.environ["TWILIO_PHONE_NUMBER"]
        self.to_number = os.environ["TWILIO_TO_PHONE_NUMBER"]

    def send_sms(self, city, flight_data):
        """Send a WhatsApp message with the deal details for the given city."""
        message = self.client.messages.create(
            body=(
                f"Low price alert!\n"
                f"Only €{flight_data.price} to fly to {city}!\n"
                f"{flight_data.origin_airport} → {flight_data.destination_airport}\n"
                f"Outbound: {flight_data.out_date}\n"
                f"Return:   {flight_data.return_date}"
            ),
            from_=f"whatsapp:{self.from_number}",
            to=f"whatsapp:{self.to_number}",
        )
        print(f"  SMS sent. SID: {message.sid}")