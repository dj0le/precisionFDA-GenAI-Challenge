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


# def wait_for_api(url="http://localhost:8000", timeout=30):
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 return True
#         except requests.ConnectionError:
#             time.sleep(0.1)
#     raise TimeoutError(f"API failed to start within {timeout} seconds")

# def start_services():
#     root_dir = Path(__file__).parent

#     # Start FastAPI
#     api_process = subprocess.Popen(
#         ["uvicorn", "main:app", "--reload"],
#         cwd=root_dir / "api"
#     )

#     # Wait for API to be ready
#     wait_for_api()

#     # Start Streamlit
#     streamlit_process = subprocess.Popen(
#         ["streamlit", "run", "streamlit_app.py"],
#         cwd=root_dir / "app"
#     )

#     try:
#         api_process.wait()
#         streamlit_process.wait()
#     except KeyboardInterrupt:
#         api_process.terminate()
#         streamlit_process.terminate()

# if __name__ == "__main__":
#     start_services()
