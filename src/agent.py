import os
import json
import sys
from groq import Groq
from retrieval import query_memory
from policy_gate import evaluate_policy
from tools import get_logs, get_metrics

# Hardcode key or load from env
GROQ_KEY = os.getenv("GROQ_API_KEY") or "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"

client = Groq(api_key=GROQ_KEY)

def run_incident_agent(service_name: str, symptoms: str, memory_enabled: bool = True):
    print("\n==========================================")
    print(f"INCIDENT INGESTED: {service_name}")
    print(f"Symptoms: {symptoms}")
    print(f"Memory Enabled: {memory_enabled}")
    print("==========================================\n")

    # 1. Gather Telemetry
    logs = get_logs(service_name)
    metrics = get_metrics(service_name)

    # 2. Memory Retrieval
    recalled_context = ""
    avoid_list = []
    
    if memory_enabled:
        items = query_memory(symptoms_text=symptoms, service_name=service_name)
        if isinstance(items, list):
            memory_texts = []
            for m in items:
                text = str(m)
                memory_texts.append(text)
                if "FAILED ATTEMPT" in text or "failed" in text.lower():
                    avoid_list.append(text)
            recalled_context = "\n".join(memory_texts)

    # 3. Construct System Prompt
    system_prompt = f"""
You are an Incident Response AI Agent. Analyze the incident using provided logs, metrics, and past memory.

TELEMETRY LOGS:
{logs}

TELEMETRY METRICS:
{metrics}

PAST MEMORIES / INCIDENTS RECALLED:
{recalled_context if recalled_context else 'None (Memory Disabled)'}

FAILED ATTEMPTS TO AVOID (CRITICAL):
{avoid_list if avoid_list else 'None'}

INSTRUCTIONS:
1. Identify the likely Root Cause.
2. Recommend the best resolution action (MUST BE EXACTLY ONE OF: "rollback_deployment", "restart_service", "flush_dns_cache"). Do NOT include extra words in recommended_action.
3. Explicitly state actions to AVOID based on past failed attempts in memory.
4. Respond ONLY in valid JSON with keys: "root_cause", "recommended_action", "avoid_actions", "confidence", "reasoning".
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": system_prompt}],
        response_format={"type": "json_object"}
    )

    recommendation = json.loads(response.choices[0].message.content)

    # 4. Policy Gate Check
    recommended_tool = recommendation.get("recommended_action", "")
    policy_check = evaluate_policy(recommended_tool, {"service": service_name})

    return {
        "recommendation": recommendation,
        "policy_check": policy_check,
        "avoid_list": avoid_list
    }

if __name__ == "__main__":
    result = run_incident_agent(
        service_name="auth-service",
        symptoms="DB connection pool exhaustion, API timeouts"
    )
    print("\n--- AGENT DECISION & RECOMMENDATION ---")
    print(json.dumps(result, indent=2))