#!/usr/bin/env python3
import subprocess, time, requests, os

# Kill any existing server
os.system('pkill -f "python3 server.py" 2>/dev/null || true')

print("Starting Luna Image Server...")
proc = subprocess.Popen(['python3', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    time.sleep(3)
    print("Testing server...")
    
    # Test API endpoint
    print("Testing GET /api/image/info...")
    response = requests.get('http://127.0.0.1:5252/api/image/info', timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    print("Server is working!")
    
    # Keep server running for 10 seconds
    time.sleep(10)
    
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Stopping server...")
    proc.terminate()
    proc.wait()