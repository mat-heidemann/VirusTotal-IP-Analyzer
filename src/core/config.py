"""
Configuration constants and settings for VirusTotal IP Analyzer
"""
import os
from pathlib import Path

# Application directories
if os.name == 'nt':  # Windows
    APPDATA_DIR = os.path.join(os.getenv("APPDATA"), "VT_IP_Analyzer")
else:  # Linux/Unix - use XDG Base Directory specification
    APPDATA_DIR = os.path.join(os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "vt-ip-analyzer")
TEMP_RESULTS_FILE = os.path.join(APPDATA_DIR, "temp_scan_results.json")
CACHE_FILE = os.path.join(APPDATA_DIR, "ip_cache.json")
API_KEY_FILE = os.path.join(APPDATA_DIR, "api_key.enc")
FERNET_KEY_FILE = os.path.join(APPDATA_DIR, "fernet.key")

# Default settings
DEFAULT_FIELDS = [
    "IP", "Process Name", "Reputation Score", "Country", "ASN Owner",
    "Engines Malicious", "Engines Suspicious", "Engines Harmless",
    "Community Malicious Votes", "Community Harmless Votes"
]
DEFAULT_OUTPUT_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "scan_output.csv")

# GUI Colors
COLOR_SELECTED = "#1E3A8A"
COLOR_UNSELECTED = "#2E2E2E"
COLOR_DISABLED = "#555555"

# API Settings
VIRUSTOTAL_BASE_URL = "https://www.virustotal.com/api/v3/ip_addresses"
MAX_RETRIES = 3
RETRY_DELAY = 10

# Scanning defaults
DEFAULT_BATCH_SIZE = 4
DEFAULT_BATCH_DELAY = 60
DEFAULT_MAX_IPS = 0  # 0 means no limit

# Create AppData directory
os.makedirs(APPDATA_DIR, exist_ok=True)
