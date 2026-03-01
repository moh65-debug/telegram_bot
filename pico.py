import os
import subprocess
import json
import sys

# --- 🔑 YOUR SETTINGS ---
OPENROUTER_KEY = "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"
TELEGRAM_TOKEN = "8578074140:AAGuXRf3bR1LjW52Oz9G6FkcG92UWtSINY4"
MY_USER_ID = "2035257746"
# ------------------------

def run_setup():
    # 1. Download Binary
    if not os.path.exists("picoclaw"):
        print("📥 Downloading PicoClaw...")
        binary_url = "https://github.com/sipeed/picoclaw/releases/download/v0.1.1/picoclaw-linux-amd64"
        subprocess.run(f"curl -L -o picoclaw {binary_url}", shell=True, check=True)
        subprocess.run("chmod +x picoclaw", shell=True, check=True)

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
    # Using .run() instead of .Popen() ensures this script doesn't exit
    try:
        subprocess.run(["./picoclaw", "gateway"], check=True)
    except KeyboardInterrupt:
        print("\nStopping bot...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_setup()
