"""
metrics.py — Metrics Collection Layer
Logs all AI pipeline metrics to MongoDB in real time.
Every query, response time, token usage, and similarity score is tracked here.
"""

import time
import datetime
from pymongo import MongoClient

# ── MongoDB Connection ─────────────────────────────
# MongoDB Atlas free tier or local MongoDB
MONGO_URI = "mongodb://localhost:27017/"   # ← Change to your MongoDB URI

client = MongoClient(MONGO_URI)
db     = client["kgb_metrics"]            # Database name
col    = db["query_logs"]                 # Collection name

# ── Metrics Logger ─────────────────────────────────
def log_metric(
    query,
    answer,
    response_time_ms,
    token_usage,
    similarity_scores,
    cache_hit=False
):
    """
    Logs a single query's metrics to MongoDB.

    Parameters:
    - query            : User's question string
    - answer           : LLM's answer string
    - response_time_ms : How long the query took in milliseconds
    - token_usage      : Estimated number of tokens used
    - similarity_scores: List of FAISS similarity scores for retrieved docs
    - cache_hit        : Whether the result was served from cache
    """

    # Calculate semantic similarity score (average of top-k scores)
    avg_similarity = round(
        sum(similarity_scores) / len(similarity_scores), 4
    ) if similarity_scores else 0.0

    # Build the metric document to store in MongoDB
    metric_doc = {
        "timestamp":        datetime.datetime.utcnow(),  # UTC timestamp
        "query":            str(query),
        "answer_length":    len(str(answer)),
        "response_time_ms": round(response_time_ms, 2),
        "token_usage":      token_usage,
        "cache_hit":        cache_hit,
        "similarity_score": avg_similarity,
        "similarity_scores": similarity_scores,
        "model":            "mistral",
        "status":           "success"
    }

    # Insert into MongoDB
    col.insert_one(metric_doc)
    return metric_doc


def get_all_metrics():
    """Fetch all logged metrics from MongoDB"""
    metrics = list(col.find({}, {"_id": 0}).sort("timestamp", -1))
    return metrics


def get_summary_stats():
    """
    Calculate summary statistics for the dashboard.
    Returns average response time, total queries, cache hit rate etc.
    """
    total = col.count_documents({})
    if total == 0:
        return {
            "total_queries":      0,
            "avg_response_time":  0,
            "avg_similarity":     0,
            "cache_hit_rate":     0,
            "total_tokens_used":  0
        }

    pipeline = [
        {"$group": {
            "_id":               None,
            "avg_response_time": {"$avg": "$response_time_ms"},
            "avg_similarity":    {"$avg": "$similarity_score"},
            "total_tokens":      {"$sum": "$token_usage"},
            "cache_hits":        {"$sum": {"$cond": ["$cache_hit", 1, 0]}}
        }}
    ]
    result = list(col.aggregate(pipeline))

    if result:
        r = result[0]
        return {
            "total_queries":      total,
            "avg_response_time":  round(r["avg_response_time"], 2),
            "avg_similarity":     round(r["avg_similarity"], 4),
            "cache_hit_rate":     round(r["cache_hits"] / total * 100, 1),
            "total_tokens_used":  int(r["total_tokens"])
        }
    return {}
