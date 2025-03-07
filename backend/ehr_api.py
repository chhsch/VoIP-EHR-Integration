import requests
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("MEDPLUM_PROJECT_ID")
CLIENT_SECRET = os.getenv("MEDPLUM_CLIENT_SECRET")
TOKEN_URL = "https://api.medplum.com/oauth2/token"
EHR_API_URL = "https://api.medplum.com/fhir/R4"

# Function to Get Access Token
def get_access_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": PROJECT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=payload)
    token_data = response.json()
    if "access_token" in token_data:
        return token_data["access_token"]
    else:
        print("Error fetching access token:", token_data)
        return None

# Function to Fetch Patient Info by Phone Number
def get_patient_info(phone):
    access_token = get_access_token()
    if not access_token:
        return {"message": "Failed to authenticate with Medplum"}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"{EHR_API_URL}/Patient", headers=headers)
    print("Medplum API Response:", response.json()) 

    if response.status_code == 200:
        patients = response.json()
        for entry in patients.get("entry", []):
            patient_data = entry.get("resource", {})
            if "telecom" in patient_data:
                for telecom in patient_data["telecom"]:
                    if telecom.get("value") == phone:
                        return patient_data

    return {"message": "Patient not found"}

def log_call_in_ehr(call_data):
    access_token = get_access_token()
    if not access_token:
        return {"message": "Failed to authenticate with Medplum"}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Correct FHIR Communication resource format
    communication_data = {
        "resourceType": "Communication",
        "status": call_data.get("call_status", "completed"),
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                        "code": "CALL",
                        "display": "Telephone Call"
                    }
                ]
            }
        ],
        "recipient": [{"reference": f"Patient/{call_data['patient_id']}"}],
        "sender": {"reference": "Practitioner/your_practitioner_id"},  
        "payload": [{"contentString": f"Call from {call_data['caller']} to {call_data['receiver']}, Duration: {call_data['call_duration']} min"}]
    }

    print("Sending Call Log to Medplum:", communication_data)  

    response = requests.post(f"{EHR_API_URL}/Communication", json=communication_data, headers=headers)
    response_json = response.json()

    print("Medplum API Response:", response_json)  

    return response_json if response.status_code in [200, 201] else {"message": "Failed to log call", "error": response_json}
