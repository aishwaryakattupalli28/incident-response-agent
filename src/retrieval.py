import os
import json
from groq import Groq

# Put your fresh Groq key here
GROQ_KEY = "gsk_YOUR_FRESH_API_KEY_HERE"

client = Groq(api_key=GROQ_KEY)

def query_memory(symptoms_text: str, service_name: str = None):
    print(f"Querying Memory for: 'Service: {service_name}. Symptoms: {symptoms_text}'...")
    
    mock_memories = [
        "FAILED ATTEMPT on incident_01 (auth-service): Action 'restart_service' failed. Reason: DB pool immediately re-exhausted.",
        "SUCCESSFUL FIX for incident_02 (auth-service): Action 'rollback_deployment' worked. Held 24h: True"
    ]
    
    return mock_memories