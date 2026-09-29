import json

def get_logs(service: str) -> str:
    """Simulates fetching recent service logs."""
    if service == "auth-service":
        return (
            "[ERROR] 2026-09-29 13:40:01 - DB connection acquisition timeout after 30000ms\n"
            "[ERROR] 2026-09-29 13:40:05 - ConnectionPoolExhausted: Active connections = 100/100\n"
            "[WARN]  2026-09-29 13:40:12 - High latency detected across /v1/auth endpoint\n"
            "[INFO]  2026-09-29 13:40:15 - Deployment v2.4.1 currently active"
        )
    elif service == "payment-gateway":
        return (
            "[WARN] 2026-09-29 13:40:01 - CPU usage threshold exceeded (98%)\n"
            "[ERROR] 2026-09-29 13:40:10 - Request timeout on /v2/charge\n"
            "[INFO] 2026-09-29 13:40:15 - Deployment v1.8.2 active"
        )
    return f"[INFO] Logs fetched for {service}: Normal operations."

def get_metrics(service: str) -> str:
    """Simulates fetching real-time service metrics."""
    if service == "auth-service":
        return json.dumps({
            "service": "auth-service",
            "cpu_utilization": "42%",
            "memory_usage": "1.2GB / 4GB",
            "db_connections_active": 100,
            "db_connections_max": 100,
            "http_5xx_rate": "18.4%"
        })
    return json.dumps({
        "service": service,
        "cpu_utilization": "15%",
        "memory_usage": "512MB",
        "http_5xx_rate": "0.0%"
    })

def restart_service(service: str) -> str:
    """Simulates restarting a service instance."""
    return f"Service '{service}' restarted successfully. Monitoring health check..."

def rollback_deployment(service: str, target_version: str = "previous") -> str:
    """Simulates rolling back a deployment version."""
    return f"Service '{service}' successfully rolled back to target version '{target_version}'."