"""
Main scanning coordinator that orchestrates IP scanning with VirusTotal
"""
import threading
import time
import csv
import os
from typing import Dict, List, Callable
from .api_client import VirusTotalClient
from .network_scanner import NetworkScanner
from .cache_manager import CacheManager


class IPScanner:
    """Coordinates IP scanning operations"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.vt_client = VirusTotalClient(api_key)
        self.network_scanner = NetworkScanner()
        self.cache_manager = CacheManager()
        self._stop_scanning = False
    
    def scan_network_ips(
        self,
        ignore_cache: bool,
        max_ips: int,
        batch_size: int,
        batch_delay: int,
        log_callback: Callable[[str], None]
    ) -> List[Dict]:
        """
        Scan network IPs and return results
        
        Args:
            ignore_cache: Whether to ignore cached results
            max_ips: Maximum number of IPs to scan (0 for no limit)
            batch_size: Number of IPs to scan in parallel
            batch_delay: Delay between batches in seconds
            log_callback: Function to call for logging
            
        Returns:
            List of scan results
        """
        self._stop_scanning = False
        log_callback("🚀 Starting IP scan...")
        
        # Clear any existing temp results
        self.cache_manager.clear_temp_results()
        
        # Load cache
        cache = self.cache_manager.load_cache()
        log_callback(f"📂 Loaded {len(cache)} cached IPs")
        
        # Get external IPs
        ip_process_map = self.network_scanner.get_external_ips(log_callback)
        
        if not ip_process_map:
            log_callback("❌ No external IPs found")
            return []
        
        # Filter cached IPs if requested
        original_count = len(ip_process_map)
        if ignore_cache:
            cached_ips = self.cache_manager.get_cached_ips()
            ip_process_map = {
                ip: proc for ip, proc in ip_process_map.items() 
                if ip not in cached_ips
            }
            filtered_count = len(ip_process_map)
            log_callback(f"🧹 Ignored {original_count - filtered_count} cached IPs. {filtered_count} remaining")
        
        # Apply IP limit
        if max_ips > 0 and len(ip_process_map) > max_ips:
            ip_items = list(ip_process_map.items())[:max_ips]
            ip_process_map = dict(ip_items)
            log_callback(f"📉 Limited to {len(ip_process_map)} IPs for this scan")
        
        if not ip_process_map:
            log_callback("ℹ️ No IPs to scan after filtering")
            return []
        
        # Perform threaded scanning
        results = self._scan_ips_threaded(
            ip_process_map, cache, batch_size, batch_delay, log_callback
        )
        
        # Save updated cache
        if self.cache_manager.save_cache(cache):
            log_callback(f"💾 Cache updated with {len(cache)} entries")
        
        # Save temporary results
        if self.cache_manager.save_temp_results(results):
            log_callback("💾 Temporary results saved")
        
        log_callback("✅ Scan completed successfully")
        return results
    
    def _scan_ips_threaded(
        self,
        ip_process_map: Dict[str, str],
        cache: Dict[str, Dict],
        batch_size: int,
        batch_delay: int,
        log_callback: Callable[[str], None]
    ) -> List[Dict]:
        """Scan IPs using threading with batching"""
        results = []
        cache_lock = threading.Lock()
        processed_ips = set()
        processed_ips_lock = threading.Lock()
        
        ip_items = list(ip_process_map.items())
        total_ips = len(ip_items)
        
        def worker(ip: str, process_name: str):
            if self._stop_scanning:
                return
                
            with processed_ips_lock:
                if ip in processed_ips:
                    return
                processed_ips.add(ip)
            
            # Check cache first
            if ip in cache:
                with cache_lock:
                    entry = cache[ip]
                log_callback(f"✅ Using cached data for {ip}")
            else:
                # Query VirusTotal
                vt_data, _ = self.vt_client.query_ip(ip, log_callback)
                if vt_data:
                    entry = {"IP": ip, "Process Name": process_name, **vt_data}
                    with cache_lock:
                        cache[ip] = entry
                    log_callback(f"🆕 Successfully scanned: {ip}")
                else:
                    entry = {"IP": ip, "Process Name": process_name}
                    log_callback(f"⚠️ Failed to scan: {ip}")
            
            with cache_lock:
                results.append(entry)
        
        # Process in batches
        for i in range(0, total_ips, batch_size):
            if self._stop_scanning:
                break
                
            batch = ip_items[i:i + batch_size]
            threads = []
            
            for ip, proc in batch:
                if self._stop_scanning:
                    break
                t = threading.Thread(target=worker, args=(ip, proc))
                threads.append(t)
                t.start()
            
            # Wait for batch to complete
            for t in threads:
                t.join()
            
            # Delay between batches (except for last batch)
            if i + batch_size < total_ips and not self._stop_scanning:
                log_callback(f"⏳ Waiting {batch_delay}s before next batch...")
                time.sleep(batch_delay)
        
        return results
    
    def stop_scanning(self):
        """Stop the current scanning operation"""
        self._stop_scanning = True
    
    def export_to_csv(
        self,
        results: List[Dict],
        selected_fields: List[str],
        csv_path: str,
        log_callback: Callable[[str], None]
    ) -> bool:
        """
        Export scan results to CSV file
        
        Args:
            results: List of scan results
            selected_fields: Fields to include in CSV
            csv_path: Path to save CSV file
            log_callback: Function to call for logging
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            
            with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=selected_fields)
                writer.writeheader()
                
                for row in results:
                    filtered_row = {k: row.get(k, "") for k in selected_fields}
                    writer.writerow(filtered_row)
            
            log_callback(f"📄 CSV exported to: {csv_path}")
            return True
            
        except Exception as e:
            log_callback(f"❌ Failed to export CSV: {str(e)}")
            return False
    
    def get_scan_summary(self, results: List[Dict]) -> Dict[str, int]:
        """
        Get summary statistics for scan results
        
        Args:
            results: List of scan results
            
        Returns:
            Dictionary with summary statistics
        """
        if not results:
            return {"total": 0, "malicious": 0, "suspicious": 0, "clean": 0}
        
        total = len(results)
        malicious = 0
        suspicious = 0
        clean = 0
        
        for result in results:
            mal_engines = result.get("Engines Malicious", 0)
            sus_engines = result.get("Engines Suspicious", 0)
            harm_engines = result.get("Engines Harmless", 0)
            
            if isinstance(mal_engines, int) and isinstance(sus_engines, int):
                if mal_engines > 0:
                    malicious += 1
                elif sus_engines > 0:
                    suspicious += 1
                else:
                    clean += 1
        
        return {
            "total": total,
            "malicious": malicious,
            "suspicious": suspicious,
            "clean": clean
        }
