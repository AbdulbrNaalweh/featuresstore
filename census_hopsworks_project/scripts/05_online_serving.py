import json
import time
import sys
import os
import numpy as np
from connection_helper import get_feature_store

print("=" * 60)
print("ONLINE SERVING TEST")
print("=" * 60)

fs, project = get_feature_store()

feature_view = fs.get_feature_view("census_features_view", version=1)

print("Initializing serving...")
feature_view.init_serving()

# --- Latency Tests ---
print("\n" + "-" * 40)
print("Latency Tests")
print("-" * 40)

num_iterations = 50
latencies = []

print(f"Running {num_iterations} queries...")

for i in range(num_iterations):
    start_time = time.time()
    features = feature_view.get_feature_vector({"row_id": i})
    elapsed_ms = (time.time() - start_time) * 1000
    latencies.append(elapsed_ms)
    if (i + 1) % 10 == 0:
        print(f"  {i + 1}/{num_iterations} done ({elapsed_ms:.1f} ms)")

latencies = np.array(latencies)

latency_stats = {
    "iterations": num_iterations,
    "mean_ms": float(np.mean(latencies)),
    "median_ms": float(np.median(latencies)),
    "p95_ms": float(np.percentile(latencies, 95)),
    "p99_ms": float(np.percentile(latencies, 99)),
    "min_ms": float(np.min(latencies)),
    "max_ms": float(np.max(latencies)),
    "std_ms": float(np.std(latencies))
}

print(f"\nLatency Results:")
print(f"  Mean:   {latency_stats['mean_ms']:.2f} ms")
print(f"  Median: {latency_stats['median_ms']:.2f} ms")
print(f"  P95:    {latency_stats['p95_ms']:.2f} ms")
print(f"  P99:    {latency_stats['p99_ms']:.2f} ms")
print(f"  Min:    {latency_stats['min_ms']:.2f} ms")
print(f"  Max:    {latency_stats['max_ms']:.2f} ms")

# --- Throughput Tests ---
print("\n" + "-" * 40)
print("Throughput Tests")
print("-" * 40)

duration_seconds = 10
print(f"Running throughput test for {duration_seconds} seconds...")

start_time = time.time()
query_count = 0

while time.time() - start_time < duration_seconds:
    feature_view.get_feature_vector({"row_id": query_count % 1000})
    query_count += 1

total_time = time.time() - start_time
throughput = query_count / total_time

throughput_stats = {
    "duration_seconds": duration_seconds,
    "total_queries": query_count,
    "queries_per_second": float(throughput)
}

print(f"\nThroughput Results:")
print(f"  Queries:     {query_count}")
print(f"  Throughput:  {throughput:.2f} qps")

# Save all results
results = {
    "latency": latency_stats,
    "throughput": throughput_stats
}

with open('../results/hopsworks_online_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: ../results/hopsworks_online_results.json")
print("=" * 60)
print("ONLINE SERVING TEST COMPLETE")
print("=" * 60)

# Bypass PyArrow Windows cleanup crash
os._exit(0)