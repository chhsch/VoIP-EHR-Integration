from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

def get_call_logs():
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        calls = client.calls.list(limit=5)

        
        for call in calls:
            print("Full Call Data:", call.__dict__)


        call_logs = []
        for call in calls:
            call_logs.append({
                "from": getattr(call, "_from", "Unknown Caller"), 
                "to": getattr(call, "to", "Unknown Receiver"),
                "status": getattr(call, "status", "Unknown Status"),
                "duration": getattr(call, "duration", "0")
            })

        return call_logs

    except Exception as e:
        return {"error": str(e)}


