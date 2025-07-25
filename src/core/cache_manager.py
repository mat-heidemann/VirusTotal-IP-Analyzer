"""
Cache management for storing and retrieving IP scan results
"""
import json
import os
from typing import Dict, List, Set, Optional
from .config import CACHE_FILE, TEMP_RESULTS_FILE


class CacheManager:
    """Manages caching of IP scan results"""
    
    def __init__(self):
        self.cache_file = CACHE_FILE
        self.temp_file = TEMP_RESULTS_FILE
    
    def load_cache(self) -> Dict[str, Dict]:
        """
        Load cached IP data from file
        
        Returns:
            Dictionary mapping IP addresses to their scan results
        """
        if not os.path.exists(self.cache_file):
            return {}
        
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
                return cache if isinstance(cache, dict) else {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load cache file: {e}")
            return {}
    
    def save_cache(self, cache: Dict[str, Dict]) -> bool:
        """
        Save cache data to file
        
        Args:
            cache: Dictionary of IP data to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error: Failed to save cache file: {e}")
            return False
    
    def get_cached_ips(self) -> Set[str]:
        """
        Get set of all cached IP addresses
        
        Returns:
            Set of IP addresses that are cached
        """
        cache = self.load_cache()
        return set(entry.get("IP", "") for entry in cache.values() if "IP" in entry)
    
    def is_ip_cached(self, ip: str) -> bool:
        """
        Check if an IP is already cached
        
        Args:
            ip: IP address to check
            
        Returns:
            True if IP is cached, False otherwise
        """
        return ip in self.get_cached_ips()
    
    def get_cached_entry(self, ip: str) -> Optional[Dict]:
        """
        Get cached entry for a specific IP
        
        Args:
            ip: IP address to look up
            
        Returns:
            Cached entry dictionary or None if not found
        """
        cache = self.load_cache()
        return cache.get(ip)
    
    def add_to_cache(self, ip: str, data: Dict) -> None:
        """
        Add or update an entry in the cache
        
        Args:
            ip: IP address
            data: Scan result data to cache
        """
        cache = self.load_cache()
        cache[ip] = data
        self.save_cache(cache)
    
    def save_temp_results(self, results: List[Dict]) -> bool:
        """
        Save temporary scan results
        
        Args:
            results: List of scan results to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.temp_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error: Failed to save temp results: {e}")
            return False
    
    def load_temp_results(self) -> List[Dict]:
        """
        Load temporary scan results
        
        Returns:
            List of scan results or empty list if file doesn't exist
        """
        if not os.path.exists(self.temp_file):
            return []
        
        try:
            with open(self.temp_file, "r", encoding="utf-8") as f:
                results = json.load(f)
                return results if isinstance(results, list) else []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load temp results: {e}")
            return []
    
    def clear_temp_results(self) -> bool:
        """
        Clear temporary results file
        
        Returns:
            True if successful or file doesn't exist, False on error
        """
        if not os.path.exists(self.temp_file):
            return True
        
        try:
            os.remove(self.temp_file)
            return True
        except OSError as e:
            print(f"Warning: Failed to remove temp file: {e}")
            return False
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get statistics about the cache
        
        Returns:
            Dictionary with cache statistics
        """
        cache = self.load_cache()
        temp_results = self.load_temp_results()
        
        return {
            "cached_ips": len(cache),
            "temp_results": len(temp_results),
            "total_unique_ips": len(set(cache.keys()) | set(r.get("IP", "") for r in temp_results))
        }
    
    def cleanup_cache(self, max_entries: int = 1000) -> int:
        """
        Clean up cache by removing oldest entries if it exceeds max_entries
        
        Args:
            max_entries: Maximum number of entries to keep
            
        Returns:
            Number of entries removed
        """
        cache = self.load_cache()
        
        if len(cache) <= max_entries:
            return 0
        
        # Sort by last analysis date if available, otherwise by IP
        sorted_items = sorted(
            cache.items(),
            key=lambda x: x[1].get("Last Analysis Date", "0000/00/00")
        )
        
        # Keep only the most recent entries
        entries_to_remove = len(cache) - max_entries
        new_cache = dict(sorted_items[entries_to_remove:])
        
        self.save_cache(new_cache)
        return entries_to_remove
