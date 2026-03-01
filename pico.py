import os
import subprocess
import json
import sys
import urllib.request

# --- 🔑 YOUR SETTINGS ---
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
MY_USER_ID = os.environ.get("MY_USER_ID")
# ------------------------

def run_setup():
    # 1. Download Binary
    if not os.path.exists("picoclaw"):
        print("📥 Downloading PicoClaw...")
        binary_url = "https://github.com/sipeed/picoclaw/releases/download/v0.1.1/picoclaw-linux-amd64"
        urllib.request.urlretrieve(binary_url, "picoclaw")
        os.chmod("picoclaw", 0o755)
        print("✅ Binary downloaded.")

    # 2. Create Config Directory & File
    config_dir = os.path.expanduser("~/.picoclaw")
    os.makedirs(config_dir, exist_ok=True)
    
    config_data = {
        "agents": {
            "defaults": {
                "model": "arcee-ai/trinity-large-preview:free",
                "max_tokens": 16384,
                "temperature": 0.7
            }
        },
        "providers": {
            "openrouter": {
                "api_key": OPENROUTER_KEY,
                "api_base": "https://openrouter.ai/api/v1"
            }
        },
        "channels": {
            "telegram": {
                "enabled": True,
                "token": TELEGRAM_TOKEN,
                "allowFrom": [MY_USER_ID]
            }
        }
    }

    with open(os.path.join(config_dir, "config.json"), "w") as f:
        json.dump(config_data, f, indent=2)
    print("✅ Config saved.")

    # 3. Launch the Gateway and STAY ALIVE
    print("🚀 Starting PicoClaw Gateway...")
    try:
        subprocess.run(["./picoclaw", "gateway"], check=True)
    except KeyboardInterrupt:
        print("\nStopping bot...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_setup()
