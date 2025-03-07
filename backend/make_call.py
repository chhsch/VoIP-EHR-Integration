from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Twilio Credentials
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = "+18446293840"  # Twilio number (with +1 for US)
TO_PHONE_NUMBER = "+12023911719"      # Your personal number (with +1 for US)


client = Client(ACCOUNT_SID, AUTH_TOKEN)

call = client.calls.create(
    to=TO_PHONE_NUMBER,
    from_=TWILIO_PHONE_NUMBER,
    url="http://demo.twilio.com/docs/voice.xml"  # Twilio demo voice message
)

print("🔹 Test Call SID:", call.sid)
