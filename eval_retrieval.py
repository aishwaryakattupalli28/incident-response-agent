import json

def calculate_metrics():
    # Load synthetic dataset
    with open("data/incidents.json", "r") as f:
        data = json.load(f)

    # Test queries
    queries = [
        {"query": "DB connection pool exhaustion", "target_id": "INC-001"},
        {"query": "High CPU saturation", "target_id": "INC-002"},
        {"query": "High memory usage 98%", "target_id": "INC-003"},
        {"query": "Order creation latency", "target_id": "INC-004"},
        {"query": "Empty search results", "target_id": "INC-005"}
    ]

    hits = 0
    reciprocal_ranks = []

    for q in queries:
        retrieved_ids = [doc["id"] for doc in data if q["query"].lower() in doc.get("symptoms", "").lower()]
        
        if q["target_id"] in retrieved_ids:
            hits += 1
            rank = retrieved_ids.index(q["target_id"]) + 1
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0.0)

    total_queries = len(queries)
    hit_rate = hits / total_queries if total_queries > 0 else 0
    mrr = sum(reciprocal_ranks) / total_queries if total_queries > 0 else 0

    print("=========================================")
    print("      HINDSIGHT RETRIEVAL EVALUATION     ")
    print("=========================================")
    print(f"Total Dataset Size : {len(data)} Incidents")
    print(f"Total Test Queries : {total_queries}")
    print(f"Hit Rate @ K       : {hit_rate * 100:.1f}%")
    print(f"MRR Score          : {mrr:.3f}")
    print("=========================================")

if __name__ == "__main__":
    calculate_metrics()