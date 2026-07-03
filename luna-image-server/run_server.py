#!/usr/bin/env python3
import os, sys

# Ensure we're in the correct directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the server from server.py
from server import app

if __name__ == '__main__':
    print("🚀 Starting Luna Image Server (MPC)...")
    print(f"📍 Image path: /workspaces/os/IMG_8347.png")
    print(f"🌐 Server will run on: http://127.0.0.1:5252")
    print()
    
    # Verify image exists
    if os.path.exists('/workspaces/os/IMG_8347.png'):
        print("✅ Image file exists")
        with open('/workspaces/os/IMG_8347.png', 'rb') as f:
            header = f.read(8)
            print(f"   Header: {header}")
    else:
        print("❌ Image file not found")
    
    print()
    print("📡 Server ready. Press Ctrl+C to stop.")
    print()
    print("Available endpoints:")
    print("  • GET /api/image/info      - Image metadata")
    print("  • GET /api/image/view      - Full-size image")
    print("  • GET /api/image           - Thumbnail")
    print("  • GET /api/images          - List all images")
    print("  • POST /api/image/upload   - Upload image")
    print("  • POST /api/process/image  - Process image")
    print("  • GET /api/search/images   - Search images")
    print("  • POST /api/compare/images  - Compare images")
    print()
    
    # Run the Flask app
    app.run(host="127.0.0.1", port=5252)
