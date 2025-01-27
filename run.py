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

    # Start Streamlit
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "streamlit_app.py"],
        cwd=root_dir / "app"
    )

    try:
        api_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        api_process.terminate()
        streamlit_process.terminate()

if __name__ == "__main__":
    start_services()
