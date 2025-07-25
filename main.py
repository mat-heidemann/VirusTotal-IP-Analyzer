#!/usr/bin/env python3
"""
VirusTotal IP Analyzer - Main Entry Point

A comprehensive network security tool that scans external IP connections,
analyzes them using VirusTotal API, and provides IP blocking capabilities.

Author: VirusTotal IP Analyzer Team
License: MIT
"""

import sys
import os

def get_resource_path():
    """Get the correct path for resources when running as PyInstaller executable"""
    if hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller executable
        return sys._MEIPASS
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def setup_paths():
    """Setup Python paths for imports"""
    base_path = get_resource_path()
    src_path = os.path.join(base_path, 'src')
    
    # Add src directory to Python path for imports
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Also add base path
    if base_path not in sys.path:
        sys.path.insert(0, base_path)

def main():
    """Main entry point for the application."""
    try:
        print("Starting VirusTotal IP Analyzer...")
        print(f"Python version: {sys.version}")
        print(f"Running from: {os.path.abspath(__file__)}")
        
        # Setup paths first
        print("Setting up paths...")
        setup_paths()
        
        base_path = get_resource_path()
        src_path = os.path.join(base_path, 'src')
        print(f"Base path: {base_path}")
        print(f"Source path: {src_path}")
        print(f"Source path exists: {os.path.exists(src_path)}")
        
        # Check if running as PyInstaller executable
        if hasattr(sys, '_MEIPASS'):
            print(f"Running as PyInstaller executable")
            print(f"_MEIPASS: {sys._MEIPASS}")
            print(f"Contents of _MEIPASS: {os.listdir(sys._MEIPASS) if os.path.exists(sys._MEIPASS) else 'Not found'}")
        else:
            print("Running as Python script")
        
        print("Current Python path:")
        for path in sys.path[:5]:  # Show first 5 paths
            print(f"  {path}")
        
        # Import after path setup
        print("Importing main window module...")
        from src.gui.main_window import VirusTotalIPAnalyzer
        
        print("Creating application instance...")
        # Create and run the application
        app = VirusTotalIPAnalyzer()
        
        print("Starting GUI...")
        app.run()
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("\nDebugging information:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python executable: {sys.executable}")
        print(f"Python path: {sys.path}")
        
        if hasattr(sys, '_MEIPASS'):
            print(f"PyInstaller temp directory: {sys._MEIPASS}")
            if os.path.exists(sys._MEIPASS):
                print("Contents of PyInstaller temp directory:")
                for item in os.listdir(sys._MEIPASS):
                    print(f"  {item}")
        
        print("\nPlease ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("\nFull traceback:")
        import traceback
        traceback.print_exc()
        
        print("\nDebugging information:")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python executable: {sys.executable}")
        
        if hasattr(sys, '_MEIPASS'):
            print(f"PyInstaller temp directory: {sys._MEIPASS}")
        
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
