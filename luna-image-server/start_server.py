import subprocess, time, signal, os

# Kill any existing server
os.system('pkill -f "python3 server.py" 2>/dev/null || true')

print("🚀 Starting Luna Image Server (MPC)...")
print(f"📍 Image path: /workspaces/os/IMG_8347.png")
print(f"🌐 Server will run on: http://127.0.0.1:5252")
print()

proc = subprocess.Popen(['python3', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    # Wait for server to start
    time.sleep(4)
    
    print("📡 Testing server connection...")
    
    # Test connection
    import requests
    response = requests.get('http://127.0.0.1:5252/api/image/info', timeout=5)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCCESS! Server is working perfectly!")
        print(f"   🖼️  Image: {data.get('filename', 'Unknown')}")
        print(f"   📏 Dimensions: {data.get('width', 0)}x{data.get('height', 0)}")
        print(f"   📊 Size: {data.get('size_bytes', 0):,} bytes")
        print(f"   🎨 Format: {data.get('format', 'Unknown')}")
        print()
        print("🎉 YOUR MPC IMAGE SERVER IS READY! 🎉")
        print()
        print("You can now access the image via:")
        print(f"   • GET http://127.0.0.1:5252/api/image/info      - Metadata")
        print(f"   • GET http://127.0.0.1:5252/api/image/view      - Full size")
        print(f"   • GET http://127.0.0.1:5252/api/image           - Thumbnail")
        print(f"   • GET http://127.0.0.1:5252/                   - Web UI")
        print()
        print("Press Ctrl+C to stop the server")
        
        # Keep server running
        while True:
            time.sleep(1)
    else:
        print(f"❌ Server returned status: {response.status_code}")
        print("\n📋 Checking server logs...")
        time.sleep(1)
        server_logs = proc.stdout.read().decode('utf-8', errors='ignore')
        server_stderr = proc.stderr.read().decode('utf-8', errors='ignore')
        print(f"Server logs: {server_logs[-1000:] if server_logs else 'No output'}")
        print(f"Server stderr: {server_stderr[-500:] if server_stderr else 'No output'}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n📋 Server logs:")
    time.sleep(1)
    try:
        server_logs = proc.stdout.read().decode('utf-8', errors='ignore')
        server_stderr = proc.stderr.read().decode('utf-8', errors='ignore')
        print(f"stdout: {server_logs[-1000:] if server_logs else 'No output'}")
        print(f"stderr: {server_stderr[-500:] if server_stderr else 'No output'}")
    except Exception as log_error:
        print(f"Failed to read logs: {log_error}")
finally:
    print("\n🛑 Stopping server...")
    proc.terminate()
    try:
        proc.wait()
    except:
        proc.kill()
