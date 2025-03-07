from fastapi import FastAPI
import requests
from twilio_api import get_call_logs
from ehr_api import EHR_API_URL, get_patient_info, log_call_in_ehr
from ehr_api import get_access_token 
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Enable CORS to allow requests from frontend (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.get("/")
def home():
    return {"message": "VoIP-EHR Integration API is running!"}

@app.get("/calls")
def fetch_calls():
    return get_call_logs()

@app.get("/patient/{phone}")
def fetch_patient(phone: str):
    return get_patient_info(phone)

@app.post("/log_call")
def log_call(call_data: dict):
    return log_call_in_ehr(call_data)

@app.get("/calls/{patient_id}")
def get_calls_for_patient(patient_id: str):
    access_token = get_access_token()
    if not access_token:
        return {"message": "Failed to authenticate with Medplum"}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Fetch call logs
    response = requests.get(f"{EHR_API_URL}/Communication?recipient=Patient/{patient_id}", headers=headers)

    if response.status_code != 200:
        return {"message": "Failed to fetch call logs"}

    call_logs = response.json().get("entry", [])

    # Extract all call logs properly
    cleaned_logs = []
    for entry in call_logs:
        resource = entry.get("resource", {})
        cleaned_logs.append({
            "call_id": resource.get("id"),
            "status": resource.get("status"),
            "recipient": resource.get("recipient", [{}])[0].get("reference"),
            "caller": resource.get("payload", [{}])[0].get("contentString"),
            "last_updated": resource.get("meta", {}).get("lastUpdated"),
        })

    print(f"🔹 Extracted {len(cleaned_logs)} call logs from Medplum")

    return {"patient_id": patient_id, "call_logs": cleaned_logs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
