import os
import sys
import json

sys.path.append(os.getcwd())

from jellyfin_mcp.jellyfin_api import Api


def load_env(env_path=".env"):
    if not os.path.exists(env_path):
        print(f"Warning: {env_path} not found.")
        return

    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip("'").strip('"')


def main():
    load_env()

    base_url = os.environ.get("JELLYFIN_INSTANCE")
    token = os.environ.get("JELLYFIN_ACCESS_TOKEN")

    if not base_url or not token:
        print(
            "Error: JELLYFIN_INSTANCE or JELLYFIN_ACCESS_TOKEN not found in environment."
        )
        return

    print(f"Testing Jellyfin API at {base_url}...")

    api = Api(base_url=base_url, token=token)

    try:
        users = api.get_users()
        print(f"Successfully retrieved {len(users)} users.")

        if len(users) > 0:
            print(f"First user sample:\n{json.dumps(users[0], indent=2)}")

        for user in users:
            print(f"- {user.get('Name')} (ID: {user.get('Id')})")
    except Exception as e:
        print(f"Error fetching users: {e}")


if __name__ == "__main__":
    main()
