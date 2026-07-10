import subprocess
import sys
import os
import time
from datetime import datetime

# Change to scripts directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_separator():
    print("\n" + "-" * 70)


def run_script(script_name, description):
    print_header(f"EXECUTING: {description}")
    print(f"  Script: {script_name}")
    print_separator()

    start_time = time.time()
    result = subprocess.run([sys.executable, script_name])
    elapsed_time = time.time() - start_time

    if result.returncode != 0:
        print(f"\n  ERROR: Failed to run {script_name}")
        print(f"  Return code: {result.returncode}")
        return False, elapsed_time

    print(f"\n  Completed in {elapsed_time:.2f} seconds")
    return True, elapsed_time


def main():
    scripts = [
        ("00_download_data.py", "Download Dataset"),
        ("01_connect.py", "Test Connection"),
        ("02_create_feature_group.py", "Create Feature Group"),
        ("03_create_feature_view.py", "Create Feature View"),
        ("04_offline_serving.py", "Offline Serving Test"),
        ("05_online_serving.py", "Online Serving Test")
    ]

    print("\n" + "*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + " " * 12 + "HOPSWORKS SERVERLESS - COMPLETE PIPELINE" + " " * 18 + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)

    start_time = time.time()
    results = []

    for script, description in scripts:
        success, script_time = run_script(script, description)
        results.append({
            "script": script,
            "description": description,
            "success": success,
            "time": script_time
        })

        if not success:
            print("\n" + "!" * 70)
            print(f"! PIPELINE STOPPED at: {description}")
            print("!" * 70)
            break

        time.sleep(1)

    total_time = time.time() - start_time

    # Summary
    print("\n" + "*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + " " * 24 + "EXECUTION SUMMARY" + " " * 27 + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)

    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total time: {total_time:.2f} seconds")
    print("\nScript Execution:")

    for r in results:
        status = "PASSED" if r['success'] else "FAILED"
        print(f"  [{status}] {r['description']}: {r['time']:.2f}s")

    # Results files
    print("\n" + "=" * 70)
    print("RESULTS FILES:")
    print("=" * 70)

    results_dir = "../results"
    if os.path.exists(results_dir):
        files = os.listdir(results_dir)
        if files:
            for f in sorted(files):
                file_path = os.path.join(results_dir, f)
                size = os.path.getsize(file_path)
                print(f"  - {f} ({size} bytes)")
        else:
            print("  No results files found")
    else:
        print("  Results directory not found")

    # Next steps
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("""
  1. View metrics:
     cat ../results/hopsworks_metrics.json

  2. View offline results:
     cat ../results/hopsworks_offline_results.json

  3. View online results:
     cat ../results/hopsworks_online_results.json

  4. View project in Hopsworks UI:
     https://eu-west.cloud.hopsworks.ai
    """)

    print("=" * 70)
    print("\nPIPELINE EXECUTION COMPLETED")
    print("=" * 70)

    # Exit with error code if any script failed
    if any(not r['success'] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()