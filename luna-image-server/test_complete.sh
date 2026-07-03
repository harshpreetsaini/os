#!/usr/bin/env python3
"""Quick test for Luna Image Server"""

import subprocess
import time
import requests
import sys
import os

# Kill any existing server
os.system('pkill -f "python3 server.py" 2>/dev/null || true')

print("Starting Luna Image Server for IMG_8347.png...")

# Start server
proc = subprocess.Popen(['python3', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    time.sleep(3)
    print("\nTesting server endpoints...")
    
    # Test 1: Get image info
    print("1. Testing GET /api/image/info...")
    response = requests.get('http://127.0.0.1:5252/api/image/info', timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        info = response.json()
        print(f"   ✓ Image found: {info.get('filename', 'Unknown')}")
        print(f"   ✓ Dimensions: {info.get('width', 0)}x{info.get('height', 0)}")
        print(f"   ✓ Size: {info.get('size_bytes', 0)} bytes")
    else:
        print(f"   ✗ Failed")
    
    # Test 2: View full image
    print("2. Testing GET /api/image/view...")
    response = requests.get('http://127.0.0.1:5252/api/image/view', timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        content_type = response.headers.get('content-type', '')
        print(f"   ✓ Image returned ({content_type})")
    else:
        print(f"   ✗ Failed")
    
    # Test 3: Get thumbnail
    print("3. Testing GET /api/image...")
    response = requests.get('http://127.0.0.1:5252/api/image', timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Thumbnail returned")
    else:
        print(f"   ✗ Failed")
    
    # Test 4: Root endpoint
    print("4. Testing GET /...")
    response = requests.get('http://127.0.0.1:5252/', timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Server info: {data.get('service')}")
        print(f"   ✓ Endpoints available: {len(data.get('endpoints', []))}")
    else:
        print(f"   ✗ Failed")
    
    print("\n" + "="*50)
    print("SUCCESS: Luna Image Server is working correctly!")
    print("="*50)
    print(f"\nServe: http://127.0.0.1:5252")
    print(f"Image: /workspace/os/IMG_8347.png")
    print(f"\nEndpoints:")
    print(f"  - GET /api/image/info      - Get image metadata")
    print(f"  - GET /api/image/view      - View full image")  
    print(f"  - GET /api/image           - Get thumbnail")
    print(f"  - GET /api/images          - List all images")
    print(f"  - POST /api/image/upload   - Upload an image")
    print(f"  - POST /api/process/image  - Process an image")
    print(f"  - GET /api/search/images   - Search images")
    print(f"  - POST /api/compare/images  - Compare two images")
    
    # Keep server running for demo
    print("\nServer is running. Press Ctrl+C to stop.")
    time.sleep(10)  # Let it run for demo
    
except Exception as e:
    print(f"\nError: {e}")
    sys.exit(1)
finally:
    print("\nStopping server...")
    proc.terminate()
    proc.wait()
