import json
import sys
import os
import time
import pandas as pd
from connection_helper import get_feature_store

print("=" * 60)
print("CREATING FEATURE GROUP")
print("=" * 60)

try:
    fs, project = get_feature_store()
    print(f"Connected to project: {project.name}")
    print(f"Feature Store: {fs.name}")
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit(1)

# Load census data
print("\nLoading census data...")
df = pd.read_csv('../data/adult.csv')
print(f"Loaded {len(df)} rows")

# Clean column names
df.columns = (
    df.columns.str.strip()
    .str.replace(' ', '_')
    .str.replace('-', '_')
)

# Add a unique ID column for online serving lookups
df['row_id'] = range(len(df))

print(f"Columns: {list(df.columns)}")

# Create feature group (NO dataframe argument)
print("\nCreating feature group...")
start_time = time.time()

try:
    census_fg = fs.get_or_create_feature_group(
        name="census_income_data",
        version=1,
        description="Census income prediction dataset",
        primary_key=["row_id"],
        online_enabled=True,
    )

    print(f"Feature group object ready: {census_fg.name} v{census_fg.version}")

    # Insert data separately
    print("Inserting data into feature group...")
    insert_result = census_fg.insert(df)
    print(f"Insert completed.")

    creation_time = time.time() - start_time

    print(f"\nFeature group created in {creation_time:.2f} seconds")
    print(f"Name: {census_fg.name}")
    print(f"Version: {census_fg.version}")

except Exception as e:
    print(f"Feature group creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Save metrics
os.makedirs('../results', exist_ok=True)
metrics = {
    "feature_group_creation": {
        "time_seconds": creation_time,
        "rows": len(df),
        "columns": len(df.columns)
    }
}

with open('../results/hopsworks_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("\nMetrics saved.")
print("=" * 60)
print("FEATURE GROUP CREATED SUCCESSFULLY")
print("=" * 60)