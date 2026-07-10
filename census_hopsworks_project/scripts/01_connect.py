import sys
from connection_helper import get_connection

print("=" * 60)
print("CONNECTING TO HOPWORKS")
print("=" * 60)

try:
    project = get_connection()
    print(f"\nSUCCESS!")
    print(f"  Project: {project.name}")
    print(f"  URL: {project.get_url()}")

    fs = project.get_feature_store()
    print(f"  Feature Store: {fs.name}")

except Exception as e:
    print(f"\nConnection failed: {e}")
    print("\nPlease check:")
    print("  1. config/config.json exists with correct api_key and host")
    print("  2. API key is valid and not expired")
    print("  3. Internet connection is working")
    sys.exit(1)

print("\n" + "=" * 60)
print("CONNECTION SUCCESSFUL")
print("=" * 60)