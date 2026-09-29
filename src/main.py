# src/main.py

import json
from agent import run_incident_agent
from executor import execute_action

def run_pipeline(service_name: str, symptoms: str):
    print("\n==================================================")
    print("      INCIDENT RESPONSE AUTOMATION PIPELINE      ")
    print("==================================================")

    # Step A: Run Agent Diagnosis & Retrieval
    agent_output = run_incident_agent(service_name, symptoms, memory_enabled=True)

    recommendation = agent_output["recommendation"]
    policy_check = agent_output["policy_check"]
    recommended_action = recommendation.get("recommended_action")

    print("\n--------------------------------------------------")
    print(f"AI DIAGNOSIS COMPLETE")
    print(f"Root Cause: {recommendation.get('root_cause')}")
    print(f"Recommended Action: {recommended_action}")
    print(f"Confidence: {recommendation.get('confidence')}")
    print(f"Policy Gate Status: {policy_check.get('status')}")
    print("--------------------------------------------------\n")

    # Step B: Policy Gate & Human-in-the-Loop Approval Logic
    status = policy_check.get("status")

    if status == "NEEDS_APPROVAL":
        print(f"⚠️ SECURITY ALERT: Action '{recommended_action}' on '{service_name}' requires human approval.")
        print(f"Reason: {policy_check.get('reason')}")

        # Prompt Human Operator
        user_approval = input("\n[HUMAN APPROVAL] Do you authorize this action? (yes/no): ").strip().lower()

        if user_approval in ["yes", "y"]:
            print("\n✅ Authorization granted by operator.")
            execution_result = execute_action(recommended_action, service_name)
            print(f"[RESULT]: {execution_result['message']}")
        else:
            print("\n❌ Action DECLINED by operator. Incident remediation aborted safely.")

    elif status == "ALLOWED":
        print("⚡ Action pre-approved by security policy. Executing automatically...")
        execution_result = execute_action(recommended_action, service_name)
        print(f"[RESULT]: {execution_result['message']}")

    elif status == "BLOCKED":
        print(f"🛑 CRITICAL SECURITY BLOCK: {policy_check.get('reason')}")
        print("Execution forbidden.")

if __name__ == "__main__":
    # Run pipeline on our incident
    run_pipeline(
        service_name="auth-service",
        symptoms="DB connection pool exhaustion, API timeouts"
    )