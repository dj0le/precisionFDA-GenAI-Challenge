import subprocess
import os
from pathlib import Path


def start_services():
    root_dir = Path(__file__).parent

    # Start FastAPI
    api_process = subprocess.Popen(
        ["uvicorn", "main:app", "--reload"],
        cwd=root_dir / "api"
    )

    print("🚀 Server starting at http://localhost:8000")

    try:
        api_process.wait()
    except KeyboardInterrupt:
        api_process.terminate()

if __name__ == "__main__":
    try:
        start_services()
    except Exception as e:
        print(f"❌ Failed to start services: {e}")
        exit(1)
