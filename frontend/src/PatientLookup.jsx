import { useState } from "react";
import axios from "axios";

export default function PatientLookup() {
  const [phone, setPhone] = useState("");
  const [patient, setPatient] = useState(null);
  const [calls, setCalls] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchPatientData = async () => {
    if (!phone) return;
  
    setLoading(true);
    setPatient(null); 
    setCalls([]); 
    try {
      // Fetch patient details
      const patientRes = await axios.get(`http://localhost:8000/patient/${phone}`);
      setPatient(patientRes.data);
  
      // Fetch call logs
      const callsRes = await axios.get(`http://localhost:8000/calls/${patientRes.data.id}`);
      
      // Ensure multiple call logs are retained and appended correctly
      setCalls((prevCalls) => [...prevCalls, ...callsRes.data.call_logs]);
    } catch (error) {
      console.error("Error fetching data:", error);
      setPatient(null);
      setCalls([]);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h2>Patient Call Log Lookup</h2>
      <input 
        type="text" 
        placeholder="Enter phone number" 
        value={phone} 
        onChange={(e) => setPhone(e.target.value)}
      />
      <button onClick={fetchPatientData} disabled={loading}>
        {loading ? "Searching..." : "Search"}
      </button>

      {patient && (
        <div className="patient-info">
          <h3>Patient Details</h3>
          <p><strong>Name:</strong> {patient.name && patient.name.length > 0 ? `${patient.name[0].given.join(" ")} ${patient.name[0].family}` : "Unknown"}</p>
          <p><strong>Gender:</strong> {patient.gender || "N/A"}</p>
          <p><strong>Birth Date:</strong> {patient.birthDate || "N/A"}</p>
          <h3>Call Logs</h3>
          {calls.length > 0 ? (
            <ul>
              {calls.map((call, index) => (
                <li key={index}>
                  <p><strong>Status:</strong> {call.status}</p>
                  <p><strong>Caller:</strong> {call.caller}</p>
                  <p><strong>Last Updated:</strong> {new Date(call.last_updated).toLocaleString()}</p>
                  <hr />
                </li>
              ))}
            </ul>
          ) : (
            <p>No call logs found.</p>
          )}
        </div>
      )}
    </div>
  );
}
