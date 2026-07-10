from feast import FeatureStore
import pandas as pd
import time
import json
import os
from datetime import datetime, timezone


class OfflineServingTest:

    def __init__(self, repo_path="."):
        self.store = FeatureStore(repo_path=repo_path)
        self.results = {"tests": [], "summary": {}}

    def generate_entity_df(self, n_entities=100):
        entity_df = pd.DataFrame({
            "user_id": range(n_entities),
            "event_timestamp": [datetime.now(timezone.utc) for _ in range(n_entities)]
        })
        return entity_df

    def test_historical_retrieval(self, n_entities, feature_list, description):
        print(f"\nTesting: {description}")
        print(f"  Entities: {n_entities}")
        print(f"  Features: {len(feature_list)}")

        entity_df = self.generate_entity_df(n_entities)

        start_time = time.time()
        training_data = self.store.get_historical_features(
            entity_df=entity_df,
            features=feature_list
        )
        result_df = training_data.to_df()
        query_time = time.time() - start_time

        result = {
            "description": description,
            "query_size": n_entities,
            "num_features": len(feature_list),
            "time_seconds": query_time,
            "throughput": n_entities / query_time,
            "result_rows": len(result_df)
        }

        print(f"    Time: {query_time:.3f} seconds")
        print(f"    Throughput: {result['throughput']:.0f} rows/second")

        return result

    def run_benchmarks(self):
        print("=" * 60)
        print("Offline Serving Benchmarks")
        print("=" * 60)

        feature_sets = {
            "basic": [
                "census_features:age",
                "census_features:education_num",
                "census_features:income"
            ],
            "standard": [
                "census_features:age",
                "census_features:education_num",
                "census_features:occupation",
                "census_features:hours_per_week",
                "census_features:income"
            ],
            "full": [
                "census_features:age",
                "census_features:workclass",
                "census_features:education",
                "census_features:education_num",
                "census_features:marital_status",
                "census_features:occupation",
                "census_features:relationship",
                "census_features:race",
                "census_features:sex",
                "census_features:capital_gain",
                "census_features:capital_loss",
                "census_features:hours_per_week",
                "census_features:native_country",
                "census_features:income"
            ]
        }

        sizes = [100, 1000, 5000]

        for name, features in feature_sets.items():
            print(f"\n{'=' * 40}")
            print(f"Feature Set: {name.upper()}")
            print(f"{'=' * 40}")

            for size in sizes:
                result = self.test_historical_retrieval(
                    size,
                    features,
                    f"{name}_{size}"
                )
                self.results["tests"].append(result)

        self.calculate_summary()
        self.save_results()

    def calculate_summary(self):
        df = pd.DataFrame(self.results["tests"])

        self.results["summary"] = {
            "total_tests": len(df),
            "avg_time_by_size": df.groupby("query_size")["time_seconds"].mean().to_dict(),
            "avg_throughput_by_size": df.groupby("query_size")["throughput"].mean().to_dict()
        }

    def save_results(self):
        results_path = "../results/feast_offline_results.json"
        os.makedirs(os.path.dirname(results_path), exist_ok=True)

        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        print(f"\nResults saved to: {results_path}")

        print("\n" + "=" * 60)
        print("Summary:")
        print("=" * 60)
        for key, value in self.results["summary"].items():
            print(f"  {key}: {value}")

    def run(self):
        self.run_benchmarks()


if __name__ == "__main__":
    test = OfflineServingTest()
    test.run()