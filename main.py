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

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point for the application."""
    try:
        from src.gui.main_window import VirusTotalIPAnalyzer
        
        # Create and run the application
        app = VirusTotalIPAnalyzer()
        app.run()
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
