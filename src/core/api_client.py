"""
VirusTotal API client for IP address analysis
"""
import requests
import time
from datetime import datetime
from typing import Dict, Tuple, Optional, Callable
from .config import VIRUSTOTAL_BASE_URL, MAX_RETRIES, RETRY_DELAY


class VirusTotalClient:
    """Client for interacting with VirusTotal API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"x-apikey": api_key}
    
    def query_ip(self, ip: str, log_callback: Callable[[str], None]) -> Tuple[Optional[Dict], bool]:
        """
        Query VirusTotal for IP information
        
        Args:
            ip: IP address to query
            log_callback: Function to call for logging messages
            
        Returns:
            Tuple of (data_dict, is_cached) where is_cached is always False for API calls
        """
        log_callback(f"🌐 Checking VirusTotal for: {ip}")
        url = f"{VIRUSTOTAL_BASE_URL}/{ip}"
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                
                if response.status_code == 429:
                    log_callback("⏳ Rate limit hit! Waiting before retry...")
                    time.sleep(RETRY_DELAY)
                    continue
                elif response.status_code == 404:
                    log_callback(f"⚠️ IP {ip} not found in VirusTotal database")
                    return self._create_empty_result(), False
                elif response.status_code != 200:
                    log_callback(f"❌ Error with {ip}: HTTP {response.status_code}")
                    if attempt == MAX_RETRIES - 1:
                        return None, False
                    continue
                
                # Success - parse the response
                data = response.json()["data"]
                return self._parse_vt_response(data), False
                
            except requests.exceptions.RequestException as e:
                log_callback(f"❌ Network error for {ip}: {str(e)}")
                if attempt == MAX_RETRIES - 1:
                    return None, False
                time.sleep(RETRY_DELAY)
        
        log_callback(f"❌ Failed to query VirusTotal for {ip} after {MAX_RETRIES} attempts")
        return None, False
    
    def _parse_vt_response(self, data: Dict) -> Dict:
        """Parse VirusTotal API response into standardized format"""
        attr = data["attributes"]
        
        # Parse last analysis date
        last_analysis_ts = attr.get("last_analysis_date")
        last_analysis_date = (
            datetime.utcfromtimestamp(last_analysis_ts).strftime("%d/%m/%Y") 
            if last_analysis_ts else "N/A"
        )
        
        # Parse analysis results
        analysis_results = {}
        for engine, result in attr.get("last_analysis_results", {}).items():
            category = result.get('category', 'N/A')
            result_text = result.get('result', 'Clean')
            analysis_results[engine] = f"{category} ({result_text})"
        
        return {
            "Reputation Score": attr.get("reputation", "N/A"),
            "Country": attr.get("country", "N/A"),
            "ASN": attr.get("asn", "N/A"),
            "ASN Owner": attr.get("as_owner", "N/A"),
            "Last Analysis Date": last_analysis_date,
            "Engines Malicious": attr.get("last_analysis_stats", {}).get("malicious", 0),
            "Engines Suspicious": attr.get("last_analysis_stats", {}).get("suspicious", 0),
            "Engines Harmless": attr.get("last_analysis_stats", {}).get("harmless", 0),
            "Community Malicious Votes": attr.get("total_votes", {}).get("malicious", 0),
            "Community Harmless Votes": attr.get("total_votes", {}).get("harmless", 0),
            "Analysis Results": analysis_results
        }
    
    def _create_empty_result(self) -> Dict:
        """Create empty result structure for IPs not found in VirusTotal"""
        return {
            "Reputation Score": "N/A",
            "Country": "N/A",
            "ASN": "N/A",
            "ASN Owner": "N/A",
            "Last Analysis Date": "N/A",
            "Engines Malicious": 0,
            "Engines Suspicious": 0,
            "Engines Harmless": 0,
            "Community Malicious Votes": 0,
            "Community Harmless Votes": 0,
            "Analysis Results": {}
        }
