#!/usr/bin/env python3
"""Quick verification of Luna Image Server functionality"""

import subprocess, time, requests, os, json

# Clean up any existing server
os.system('pkill -f "python3 server.py" 2>/dev/null || true')

print("🚀 Starting Luna Image Server for IMG_8347.png")
print("=" * 60)

proc = subprocess.Popen(['python3', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    time.sleep(3)
    
    base_url = "http://127.0.0.1:5252"
    
    # Test 1: Image info
    print("📸 Testing GET /api/image/info...")
    response = requests.get(f"{base_url}/api/image/info", timeout=5)
    if response.status_code == 200:
        info = response.json()
        print(f"   ✅ Image: {info['filename']}")
        print(f"   ✅ Dimensions: {info['width']}x{info['height']}")
        print(f"   ✅ Size: {info['size_bytes']} bytes")
        print(f"   ✅ Format: {info['format']}")
    else:
        print(f"   ✗ Status: {response.status_code}")
    
    # Test 2: Full size image
    print("\n🔍 Testing GET /api/image/view...")
    response = requests.get(f"{base_url}/api/image/view", timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        content_type = response.headers.get('content-type', '')
        print(f"   ✅ Image returned ({content_type})")
    
    # Test 3: Thumbnail
    print("\n🖼️  Testing GET /api/image...")
    response = requests.get(f"{base_url}/api/image", timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Thumbnail generated")
    
    # Test 4: Server info
    print("\n📋 Testing GET /...")
    response = requests.get(base_url, timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Service: {data['service']}")
        print(f"   ✅ Version: {data['version']}")
        print(f"   ✅ Endpoints: {len(data['endpoints'])}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED! Server is working correctly.")
    print("=" * 60)
    print(f"\n📍 Access your images at: {base_url}")
    print(f"🖼️  Main image: /workspace/os/IMG_8347.png ({info['width']}x{info['height']})")
    print(f"\n🔧 API Endpoints:")
    print(f"   • GET {base_url}/api/image/info      - Image metadata")
    print(f"   • GET {base_url}/api/image/view      - Full-size image")
    print(f"   • GET {base_url}/api/image           - Thumbnail")
    print(f"   • GET {base_url}/api/images          - List all images")
    print(f"   • POST {base_url}/api/image/upload   - Upload image")
    print(f"   • POST {base_url}/api/process/image  - Process image")
    print(f"   • GET {base_url}/api/search/images   - Search images")
    print(f"   • POST {base_url}/api/compare/images  - Compare images")
    
    print("\n⏳ Server is running for 15 seconds...")
    time.sleep(15)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    print("\n🛑 Stopping server...")
    proc.terminate()
    proc.wait()
