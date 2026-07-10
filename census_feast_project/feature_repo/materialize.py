from feast import FeatureStore
import pandas as pd
import time
import json
import os
from datetime import datetime
from definitions import user, census_features_view


class FeastMaterializer:

    def __init__(self, repo_path="."):
        self.repo_path = repo_path
        self.store = None
        self.metrics = {}

    def initialize_store(self):
        print("Initializing Feature Store...")
        start_time = time.time()
        self.store = FeatureStore(repo_path=self.repo_path)
        self.metrics["setup_time"] = time.time() - start_time
        print(f"Initialized in {self.metrics['setup_time']:.3f} seconds")

    def apply_definitions(self):
        print("Applying feature definitions...")
        start_time = time.time()

        # Corrected: Pass the objects to apply
        self.store.apply([user, census_features_view])

        self.metrics["apply_time"] = time.time() - start_time
        print(f"Applied in {self.metrics['apply_time']:.3f} seconds")

        entities = self.store.list_entities()
        print(f"\nRegistered Entities ({len(entities)}):")
        for entity in entities:
            print(f"  - {entity.name}")

        feature_views = self.store.list_feature_views()
        print(f"\nRegistered Feature Views ({len(feature_views)}):")
        for fv in feature_views:
            print(f"  - {fv.name}: {len(fv.schema)} features")

    def load_dataframe(self):
        data_path = "../data/processed/census_data.parquet"
        print(f"\nLoading data from: {data_path}")
        df = pd.read_parquet(data_path)
        print(f"Loaded {len(df)} rows")
        return df

    def materialize_to_online_store(self, df, batch_size=5000):
        print("\nMaterializing to Online Store (SQLite)...")
        print(f"Total rows: {len(df)}")
        print(f"Batch size: {batch_size}")

        start_time = time.time()
        total_batches = (len(df) + batch_size - 1) // batch_size

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            self.store.write_to_online_store(
                feature_view_name="census_features",
                df=batch
            )

            batch_num = i // batch_size + 1
            if batch_num % 10 == 0 or batch_num == total_batches:
                progress = (batch_num / total_batches) * 100
                print(f"  Progress: {progress:.1f}% ({batch_num}/{total_batches} batches)")

        self.metrics["materialize_time"] = time.time() - start_time
        print(f"\nMaterialization completed in {self.metrics['materialize_time']:.3f} seconds")
        print(f"Average time per row: {(self.metrics['materialize_time'] / len(df)) * 1000:.3f} ms")
        print(f"Throughput: {len(df) / self.metrics['materialize_time']:.0f} rows/second")

    def verify_online_store(self):
        print("\nVerifying Online Store...")
        result = self.store.get_online_features(
            features=["census_features:age", "census_features:occupation", "census_features:income"],
            entity_rows=[{"user_id": 0}]
        ).to_dict()
        print("Test query successful:")
        print(f"  Age: {result['age'][0]}")
        print(f"  Occupation: {result['occupation'][0]}")
        print(f"  Income: {result['income'][0]}")

    def save_metrics(self):
        self.metrics["total_time"] = sum(self.metrics.values())
        self.metrics["timestamp"] = datetime.now().isoformat()

        metrics_path = "../results/feast_metrics.json"
        os.makedirs(os.path.dirname(metrics_path), exist_ok=True)

        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)

        print(f"\nMetrics saved to: {metrics_path}")

    def run(self):
        total_start = time.time()

        self.initialize_store()
        self.apply_definitions()
        df = self.load_dataframe()
        self.materialize_to_online_store(df)
        self.verify_online_store()
        self.save_metrics()

        total_time = time.time() - total_start

        print("\n" + "=" * 50)
        print("Performance Summary:")
        print("=" * 50)
        print(f"  Setup time:       {self.metrics['setup_time']:.3f} s")
        print(f"  Apply time:       {self.metrics['apply_time']:.3f} s")
        print(f"  Materialize time: {self.metrics['materialize_time']:.3f} s")
        print(f"  Total time:       {total_time:.3f} s")
        print("=" * 50)


if __name__ == "__main__":
    materializer = FeastMaterializer()
    materializer.run()