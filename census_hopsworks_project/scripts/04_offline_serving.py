import json
import time
import sys
import os
from connection_helper import get_feature_store

print("=" * 60)
print("OFFLINE SERVING TEST")
print("=" * 60)

fs, project = get_feature_store()

feature_view = fs.get_feature_view("census_features_view", version=1)

print("\nCreating training data...")
start_time = time.time()

training_data_version, metadata = feature_view.create_training_data()

creation_time = time.time() - start_time

print(f"Training data materialized in {creation_time:.2f} seconds")
print(f"Training data version: {training_data_version}")

print("Fetching training data...")
fetch_start = time.time()
features_df, labels_df = feature_view.get_training_data(training_data_version)
fetch_time = time.time() - fetch_start

print(f"Data fetched in {fetch_time:.2f} seconds")

df = features_df.copy()
df["income"] = labels_df

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nSample data:")
print(df.head(3).to_string())

results = {
    "operation": "create_training_data",
    "time_seconds": creation_time,
    "fetch_time_seconds": fetch_time,
    "rows": int(len(df)),
    "columns": int(len(df.columns))
}

with open('../results/hopsworks_offline_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: ../results/hopsworks_offline_results.json")
print("=" * 60)
print("OFFLINE SERVING TEST COMPLETE")
print("=" * 60)

# Bypass PyArrow Windows cleanup crash
os._exit(0)