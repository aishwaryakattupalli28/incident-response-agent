# Code-enforced Safety Policy Gate

ALLOWED_TOOLS = [
    "get_logs",
    "get_metrics",
    "check_service_status",
    "search_incidents",
    "restart_service",
    "rollback_deployment",
    "flush_dns_cache",
    "clear_and_rotate_logs"
]

HIGH_RISK_TOOLS = [
    "restart_service",
    "rollback_deployment",
    "flush_dns_cache",
    "clear_and_rotate_logs"
]

CRITICAL_SERVICES = ["auth-service", "payment-gateway"]

# src/policy_gate.py

def evaluate_policy(action: str, context: dict) -> dict:
    # Normalize action string in case LLM appends extra words
    action_clean = action.lower()
    
    if "rollback" in action_clean:
        action_clean = "rollback_deployment"
    elif "restart" in action_clean:
        action_clean = "restart_service"
    elif "flush" in action_clean or "dns" in action_clean:
        action_clean = "flush_dns_cache"

    service = context.get("service", "")

    # Rule 1: Rollback on critical services requires human approval
    if action_clean == "rollback_deployment":
        return {
            "status": "NEEDS_APPROVAL",
            "reason": f"Action 'rollback_deployment' on critical service '{service}' requires human approval."
        }
    
    # Rule 2: Safe automated actions
    elif action_clean in ["restart_service", "flush_dns_cache"]:
        return {
            "status": "ALLOWED",
            "reason": f"Action '{action_clean}' is pre-approved for automated execution."
        }

    # Default fallback
    return {
        "status": "DENIED",
        "reason": f"Action '{action}' is not in the list of allowed policy actions."
    }

if __name__ == "__main__":
    # Verification tests
    print(evaluate_policy("get_logs", {"service": "auth-service"}))
    print(evaluate_policy("rollback_deployment", {"service": "auth-service"}))
    print(evaluate_policy("delete_database", {"service": "auth-service"}))