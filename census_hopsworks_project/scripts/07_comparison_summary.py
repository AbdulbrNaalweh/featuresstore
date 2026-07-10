import json
import os
import sys
from datetime import datetime

print("=" * 70)
print("FEAST vs HOPWORKS - COMPARISON SUMMARY")
print("=" * 70)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# Hopsworks results
hw_metrics_path = "../results/hopsworks_metrics.json"
hw_online_path = "../results/hopsworks_online_results.json"
hw_offline_path = "../results/hopsworks_offline_results.json"

print("\n" + "-" * 70)
print("HOPWORKS SERVERLESS RESULTS")
print("-" * 70)

hw_data = {}

# Load Feature Group metrics
if os.path.exists(hw_metrics_path):
    with open(hw_metrics_path, 'r') as f:
        hw_metrics = json.load(f)

    if "feature_group_creation" in hw_metrics:
        fg = hw_metrics["feature_group_creation"]
        hw_data["fg_time"] = fg.get("time_seconds", 0)
        hw_data["fg_rows"] = fg.get("rows_inserted", 0)
        hw_data["fg_throughput"] = fg.get("throughput_rows_per_sec", 0)

        print(f"\nFeature Group Creation:")
        print(f"  Time: {hw_data['fg_time']:.2f} seconds")
        print(f"  Rows: {hw_data['fg_rows']}")
        print(f"  Throughput: {hw_data['fg_throughput']:.0f} rows/sec")

    if "feature_view_creation" in hw_metrics:
        fv = hw_metrics["feature_view_creation"]
        hw_data["fv_time"] = fv.get("time_seconds", 0)
        hw_data["fv_features"] = fv.get("num_features", 0)

        print(f"\nFeature View Creation:")
        print(f"  Time: {hw_data['fv_time']:.2f} seconds")
        print(f"  Features: {hw_data['fv_features']}")

    if "online_serving" in hw_metrics:
        os_data = hw_metrics["online_serving"]
        hw_data["latency_mean"] = os_data.get("latency_mean_ms", 0)
        hw_data["latency_p95"] = os_data.get("latency_p95_ms", 0)
        hw_data["throughput"] = os_data.get("throughput_qps", 0)

# Load Online results
if os.path.exists(hw_online_path):
    with open(hw_online_path, 'r') as f:
        hw_online = json.load(f)

    if "latency" in hw_online and "mean_ms" in hw_online["latency"]:
        print(f"\nOnline Serving:")
        print(f"  Latency (mean): {hw_online['latency']['mean_ms']:.2f} ms")
        print(f"  Latency (P95): {hw_online['latency']['p95_ms']:.2f} ms")
        print(f"  Latency (P99): {hw_online['latency']['p99_ms']:.2f} ms")

    if "throughput" in hw_online:
        print(f"  Throughput: {hw_online['throughput']['throughput_qps']:.2f} qps")

# Load Offline results
if os.path.exists(hw_offline_path):
    with open(hw_offline_path, 'r') as f:
        hw_offline = json.load(f)

    print(f"\nOffline Serving:")
    print(f"  Time: {hw_offline.get('time_seconds', 0):.2f} seconds")
    print(f"  Rows: {hw_offline.get('rows', 0)}")
    print(f"  Columns: {hw_offline.get('columns', 0)}")

print("\n" + "-" * 70)
print("COMPARISON TABLE")
print("-" * 70)

print("""
+--------------------------+------------------------+------------------------+
|        CRITERION         |   FEAST (Local/SQLite) |  HOPWORKS (Serverless) |
+--------------------------+------------------------+------------------------+
| Setup Complexity         | Low (pip install)      | Medium (API key)       |
| Infrastructure Required  | None                   | Cloud Account          |
| Online Store             | SQLite (local)         | Managed Cloud          |
| Offline Store            | Parquet files          | Managed Cloud          |
| Scalability              | Single machine         | Cloud-scale            |
| Data Governance          | Limited                | Built-in               |
| Feature Lineage          | Basic                  | Full                   |
| Monitoring               | Manual                 | Built-in Dashboard     |
| Cost                     | Free                   | Free tier available    |
| Best Use Case            | Dev/Test, Small Data   | Production, Teams      |
+--------------------------+------------------------+------------------------+
""")

print("\n" + "-" * 70)
print("RECOMMENDATIONS")
print("-" * 70)

print("""
Choose FEAST when:
  - You need local development without internet
  - You want full control over infrastructure
  - You have a small dataset (< 1M rows)
  - You want to integrate with existing data stack
  - You need offline-first development

Choose HOPWORKS when:
  - You need production-ready feature store
  - You want managed infrastructure
  - You need team collaboration features
  - You require built-in monitoring and lineage
  - You have large-scale requirements
  - You want to reduce operational overhead
""")

print("\n" + "-" * 70)
print("CONCLUSION")
print("-" * 70)

print("""
Based on the test results and architectural analysis:

1. Feast is ideal for:
   - Research and experimentation
   - Local development environments
   - Projects with existing infrastructure

2. Hopsworks is ideal for:
   - Production ML pipelines
   - Enterprise teams
   - Projects requiring governance and lineage

The choice depends on your specific use case, team size, and
production requirements. Both tools effectively solve the
feature store problem but with different trade-offs in terms
of operational complexity and feature completeness.
""")

print("=" * 70)
print("END OF COMPARISON")
print("=" * 70)