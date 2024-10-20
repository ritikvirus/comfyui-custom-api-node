# __init__.py

import os
import subprocess
import sys
import threading

def kill_process_on_port(port):
    try:
        # Kill process on Unix/Linux/Mac
        result = subprocess.check_output(f"lsof -ti:{port}", shell=True)
        pids = result.decode().strip().split('\n')
        for pid in pids:
            if pid:
                os.kill(int(pid), 9)
    except subprocess.CalledProcessError:
        try:
            # Kill process on Windows
            result = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True)
            lines = result.decode().strip().split('\n')
            for line in lines:
                if line:
                    parts = line.strip().split()
                    pid = parts[-1]
                    subprocess.call(f"taskkill /PID {pid} /F", shell=True)
        except Exception as e:
            print(f"Could not kill process on port {port}: {e}")

def start_api():
    # Path to your API script
    api_script = os.path.join(os.path.dirname(__file__), 'api.py')
    subprocess.Popen([sys.executable, api_script])

# Kill the process and start the API when ComfyUI initializes
def init():
    port = 5000
    kill_process_on_port(port)
    threading.Thread(target=start_api).start()

