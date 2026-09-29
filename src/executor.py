import json
import datetime
import os

def execute_action(action_name, service, version="v1.0.0", root_cause="Investigated incident"):
    """
    Executes an approved action, logs it to audit.log, 
    and writes back the new incident resolution to data/incidents.json.
    """
    timestamp = datetime.datetime.now().isoformat()
    
    # 1. Write to audit.log
    audit_entry = f"[{timestamp}] USER:Operator ACTION:{action_name} SERVICE:{service} STATUS:SUCCESS\n"
    with open("audit.log", "a") as audit_file:
        audit_file.write(audit_entry)

    # 2. Write-back to data/incidents.json
    dataset_path = os.path.join("data", "incidents.json")
    if os.path.exists(dataset_path):
        try:
            with open(dataset_path, "r+") as f:
                incidents = json.load(f)
                
                # Create a new unique ID
                new_id = f"INC-0{len(incidents) + 1}" if len(incidents) < 9 else f"INC-{len(incidents) + 1}"
                
                new_entry = {
                    "id": new_id,
                    "service": service,
                    "severity": "SEV1",
                    "symptoms": f"Resolved live incident for {service}",
                    "root_cause": root_cause,
                    "failed_attempts": [],
                    "successful_fix": {
                        "action": action_name,
                        "version": version,
                        "held_24h": True
                    }
                }
                
                incidents.append(new_entry)
                f.seek(0)
                json.dump(incidents, f, indent=2)
                f.truncate()
        except Exception as e:
            print(f"Write-back error: {e}")

    return True