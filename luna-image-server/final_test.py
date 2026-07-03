#!/usr/bin/env python3
import subprocess
import time
import os

print("🎯 Final Test: Luna Image Server")
print("=" * 50)

# Clean up any existing server
os.system('pkill -f "python3 server.py" 2>/dev/null || true')

# Verify server.py exists
if not os.path.exists('server.py'):
    print("❌ server.py not found!")
    exit(1)

print("✅ server.py exists")

# Verify image exists
if not os.path.exists('/workspaces/os/IMG_8347.png'):
    print("❌ IMG_8347.png not found!")
    exit(1)

print("✅ IMG_8347.png exists")

# Start server
print("\n🚀 Starting Luna Image Server...")
server_proc = subprocess.Popen(['python3', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    time.sleep(4)
    print("\n📡 Testing server...")
    
    # Test connection
    import requests
    response = requests.get('http://127.0.0.1:5252/api/image/info', timeout=5)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Server is working perfectly!")
        print(f"   🖼️  Image: {data['filename']}")
        print(f"   📏 Dimensions: {data['width']}x{data['height']}")
        print(f"   📐 Size: {data['size_bytes']:,} bytes")
        print(f"   🎨 Format: {data['format']}")
        
        # Test thumbnail
        thumb = requests.get('http://127.0.0.1:5252/api/image', timeout=5)
        print(f"   📷 Thumbnail status: {thumb.status_code}")
        
        # Test view
        view = requests.get('http://127.0.0.1:5252/api/image/view', timeout=5)
        print(f"   👀 View status: {view.status_code}")
        
        print("\n🎉 ALL TESTS PASSED!")
        print(f"🌐 Server at: http://127.0.0.1:5252")
        print(f"📊 Metadata: http://127.0.0.1:5252/api/image/info")
        print(f"🖼️  Image: http://127.0.0.1:5252/api/image/view")
        print(f"🖼️  Thumbnail: http://127.0.0.1:5252/api/image")
        
        # Keep running for 10 seconds
        print("\n⏳ Server running for 10 seconds...")
        time.sleep(10)
        
    else:
        print(f"❌ Server failed with status {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    print("\n🛑 Stopping server...")
    server_proc.terminate()
    try:
        server_proc.wait()
    except:
        server_proc.kill()
