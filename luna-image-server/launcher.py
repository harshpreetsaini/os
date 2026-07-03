#!/usr/bin/env python3
"""Luna Image Server Launcher - MPC Server for Image Operations."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import app

if __name__ == "__main__":
    print("Starting Luna OS Image Server on http://127.0.0.1:5252")
    print("Press Ctrl+C to stop the server")
    print("Available endpoints:")
    print("  - GET /api/image/info - Get image metadata")
    print("  - GET /api/image/view - View full-size image")
    print("  - GET /api/image - Get thumbnail")
    print("  - GET /api/images - List all uploaded images")
    print("  - POST /api/image/upload - Upload an image")
    print("  - POST /api/process/image - Process an image")
    print("  - GET /api/search/images - Search images")
    print("  - POST /api/compare/images - Compare two images")
    print()
    
    try:
        app.run(host="127.0.0.1", port=5252, debug=False)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
