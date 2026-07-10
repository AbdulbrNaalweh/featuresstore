import json
import time
from connection_helper import get_feature_store

print("=" * 60)
print("CREATING FEATURE VIEW")
print("=" * 60)

fs, project = get_feature_store()
print(f"Connected to project: {project.name}")

census_fg = fs.get_feature_group("census_income_data", version=1)

print("Creating query...")
query = census_fg.select([
    "row_id",
    "age",
    "workclass",
    "education",
    "education_num",
    "marital_status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital_gain",
    "capital_loss",
    "hours_per_week",
    "native_country",
    "income"  # <-- THIS WAS MISSING
])

print("Creating Feature View...")
start_time = time.time()

feature_view = fs.get_or_create_feature_view(
    name="census_features_view",
    version=1,
    query=query,
    labels=["income"]
)

creation_time = time.time() - start_time

print(f"Feature View created in {creation_time:.2f} seconds")
print(f"Name: {feature_view.name}")
print(f"Version: {feature_view.version}")

# Update metrics
with open('../results/hopsworks_metrics.json', 'r') as f:
    metrics = json.load(f)

metrics["feature_view_creation"] = {
    "time_seconds": creation_time
}

with open('../results/hopsworks_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("\nMetrics updated.")
print("=" * 60)
print("FEATURE VIEW CREATED SUCCESSFULLY")
print("=" * 60)