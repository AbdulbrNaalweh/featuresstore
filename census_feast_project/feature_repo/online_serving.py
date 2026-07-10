from feast import FeatureStore
import time
import json
import os
import numpy as np
from datetime import datetime


class OnlineServingTest:

    def __init__(self, repo_path="."):
        self.store = FeatureStore(repo_path=repo_path)
        self.results = {}

    def test_latency(self, num_iterations=100):
        print(f"Testing latency with {num_iterations} queries...")

        feature_sets = {
            "minimal": ["census_features:age", "census_features:income"],
            "standard": [
                "census_features:age",
                "census_features:education_num",
                "census_features:occupation",
                "census_features:income"
            ],
            "full": [
                "census_features:age",
                "census_features:workclass",
                "census_features:education",
                "census_features:education_num",
                "census_features:marital_status",
                "census_features:occupation",
                "census_features:hours_per_week",
                "census_features:income"
            ]
        }

        latency_results = {}

        for name, features in feature_sets.items():
            print(f"\n  Testing: {name} ({len(features)} features)")
            latencies = []

            for i in range(num_iterations):
                start_time = time.time()

                self.store.get_online_features(
                    features=features,
                    entity_rows=[{"user_id": i % 1000}]
                ).to_dict()

                latencies.append((time.time() - start_time) * 1000)

            latencies = np.array(latencies)

            stats = {
                "feature_set": name,
                "num_features": len(features),
                "iterations": num_iterations,
                "mean_ms": float(np.mean(latencies)),
                "median_ms": float(np.median(latencies)),
                "p95_ms": float(np.percentile(latencies, 95)),
                "p99_ms": float(np.percentile(latencies, 99)),
                "min_ms": float(np.min(latencies)),
                "max_ms": float(np.max(latencies)),
                "std_ms": float(np.std(latencies))
            }

            latency_results[name] = stats

            print(f"    Mean: {stats['mean_ms']:.2f} ms")
            print(f"    P95: {stats['p95_ms']:.2f} ms")
            print(f"    P99: {stats['p99_ms']:.2f} ms")

        return latency_results

    def test_throughput(self, duration_seconds=10):
        print(f"\nTesting throughput for {duration_seconds} seconds...")

        feature_sets = {
            "minimal": ["census_features:age", "census_features:income"],
            "standard": [
                "census_features:age",
                "census_features:education_num",
                "census_features:occupation",
                "census_features:income"
            ]
        }

        throughput_results = {}

        for name, features in feature_sets.items():
            print(f"\n  Testing: {name} ({len(features)} features)")

            start_time = time.time()
            query_count = 0

            while time.time() - start_time < duration_seconds:
                self.store.get_online_features(
                    features=features,
                    entity_rows=[{"user_id": query_count % 1000}]
                ).to_dict()
                query_count += 1

            total_time = time.time() - start_time
            throughput = query_count / total_time

            stats = {
                "feature_set": name,
                "num_features": len(features),
                "duration_seconds": total_time,
                "total_queries": query_count,
                "throughput_qps": throughput
            }

            throughput_results[name] = stats

            print(f"    Total queries: {query_count}")
            print(f"    Throughput: {throughput:.2f} queries/second")

        return throughput_results

    def run(self):
        print("=" * 60)
        print("Online Serving Benchmarks")
        print("=" * 60)

        print("\n" + "-" * 40)
        print("LATENCY TESTS")
        print("-" * 40)

        self.results["latency"] = self.test_latency(100)

        print("\n" + "-" * 40)
        print("THROUGHPUT TESTS")
        print("-" * 40)

        self.results["throughput"] = self.test_throughput(10)
        self.results["timestamp"] = datetime.now().isoformat()

        results_path = "../results/feast_online_results.json"
        os.makedirs(os.path.dirname(results_path), exist_ok=True)

        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    test = OnlineServingTest()
    test.run()