#!/usr/bin/env python3
"""Luna OS Image Server - Installation script."""

import os
import sys

def main():
    print("Luna OS Image Server Installation")
    print("===============================\n")
    
    # Check for Flask and Pillow
    try:
        import flask
        import PIL
        print(f"Flask {flask.__version__} and Pillow {PIL.__version__} are available")
    except ImportError as e:
        print(f"✗ Missing dependencies: {e}")
        print("\nInstall with:")
        print("  pip3 install flask pillow")
        sys.exit(1)
    
    # Create directories
    print("\nCreating directories...")
    os.makedirs("/workspace/uploads", exist_ok=True)
    os.makedirs("/workspace/static", exist_ok=True)
    print("✓ Directories created")
    
    print("\nInstallation complete!")
    print("\nTo start the server:")
    print("  python3 /opt/luna-image-server/launcher.py")
    print("\nServer will be available at: http://127.0.0.1:5252")

if __name__ == "__main__":
    main()
