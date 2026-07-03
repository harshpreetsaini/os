#!/usr/bin/env python3
import socket
import subprocess
import time
import os

def check_port(host, port):
    """Check if port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    print("🚀 Simple MPC Server Test")
    print("=" * 50)
    
    # Check if server.py exists
    if not os.path.exists('server.py'):
        print("❌ server.py not found!")
        return
    
    print(f"✅ server.py exists")
    
    # Check if image exists
    if os.path.exists('/workspaces/os/IMG_8347.png'):
        print(f"✅ Image file exists")
        import PIL
        print(f"✅ PIL is available")
    else:
        print(f"❌ Image file not found at /workspaces/os/IMG_8347.png")
        return
    
    # Start the server
    print("\n🔧 Starting Luna Image Server...")
    try:
        server_process = subprocess.Popen(
            ['python3', 'server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        time.sleep(5)
        
        # Check if port is open
        print("🌐 Checking if server is listening...")
        if check_port('127.0.0.1', 5252):
            print("✅ Port 5252 is open - server is running!")
        else:
            print("❌ Port 5252 is not open")
            
            # Print any error messages from server
            stderr = server_process.stderr.read()
            if stderr:
                print(f"Server stderr:\n{stderr}")
            return
        
        # Test with curl
        print("\n📡 Testing with curl...")
        import subprocess
        result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://127.0.0.1:5252/api/image/info'], 
                              capture_output=True, text=True)
        
        if result.stdout == '200':
            print("✅ HTTP 200 response - server is responding correctly!")
            
            # Get response
            import json
            response = subprocess.run(['curl', '-s', 'http://127.0.0.1:5252/api/image/info'], 
                                    capture_output=True, text=True)
            data = json.loads(response.stdout)
            
            print(f"\n📊 Server Response:")
            print(f"   🖼️  Image: {data.get('filename', 'Unknown')}")
            print(f"   📏 Dimensions: {data.get('width', 0)}x{data.get('height', 0)}")
            print(f"   📐 Size: {data.get('size_bytes', 0):,} bytes")
            print(f"   🎨 Format: {data.get('format', 'Unknown')}")
            
            print("\n🎉 SUCCESS! Luna Image Server is fully operational!")
            print(f"🌐 Access at: http://127.0.0.1:5252")
            
        else:
            print(f"❌ Unexpected HTTP status: {result.stdout}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Always kill the server
        server_process.terminate()
        try:
            server_process.wait()
        except:
            server_process.kill()
        print("\n🛑 Server stopped")

if __name__ == '__main__':
    main()
