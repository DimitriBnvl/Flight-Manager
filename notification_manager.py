import os
import smtplib
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:
    """Sends flight deal alerts via WhatsApp (Twilio) and email (SMTP)."""
    def __init__(self):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"],
        )
        self.from_number = os.environ["TWILIO_PHONE_NUMBER"]
        self.to_number = os.environ["TWILIO_TO_PHONE_NUMBER"]

        self.smtp_address = os.environ["SMTP_ADDRESS"]
        self.email = os.environ["EMAIL_ADDRESS"]
        self.password = os.environ["EMAIL_APP_PASSWORD"]

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

    def send_emails(self, customer_emails, city, flight_data):
        """Send a deal alert email to every customer in customer_emails."""
        body = (
            f"Low price alert!\n\n"
            f"Only EUR {flight_data.price} to fly to {city}!\n"
            f"{flight_data.origin_airport} -> {flight_data.destination_airport}\n"
            f"Outbound: {flight_data.out_date}\n"
            f"Return:   {flight_data.return_date}\n"
            f"Stops:    {flight_data.stops}"
        )
        with smtplib.SMTP(self.smtp_address, port=587, timeout=15) as connection:
            connection.starttls()
            connection.login(self.email, self.password)
            for customer in customer_emails:
                to_address = customer["email"]
                connection.sendmail(
                    from_addr=self.email,
                    to_addrs=to_address,
                    msg=f"Subject:Low Price Alert - {city}!\n\n{body}",
                )
                print(f"  Email sent to {to_address}.")