import subprocess
import sys
import os


def run_script(script_name):
    print("\n" + "=" * 60)
    print(f"Running: {script_name}")
    print("=" * 60)

    result = subprocess.run([sys.executable, script_name])

    if result.returncode != 0:
        print(f"Error running {script_name}")
        return False
    return True


def main():
    scripts = [
        "data_ingestion.py",
        "materialize.py",
        "offline_serving.py",
        "online_serving.py"
    ]

    for script in scripts:
        if not run_script(script):
            print(f"Execution stopped due to error in {script}")
            break

    print("\n" + "=" * 60)
    print("All scripts completed")
    print("=" * 60)
    print("\nTo start the API server:")
    print("  python api_server.py")
    print("\nTo test the API:")
    print('  curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d "{\\"user_id\\": 0}"')


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()