#!/usr/bin/env python3
"""
Test script to verify network scanning functionality
"""
from network_scanner import NetworkScanner

def main():
    print("🔍 Testing Network Scanner on Linux...")
    print("=" * 50)
    
    scanner = NetworkScanner()
    
    def log_callback(msg):
        print(f"[LOG] {msg}")
    
    # Test network scanning
    external_ips = scanner.get_external_ips(log_callback)
    
    print("\n📊 Results:")
    print("=" * 50)
    
    if external_ips:
        print(f"✅ Found {len(external_ips)} external IP connections:")
        for ip, process in external_ips.items():
            print(f"  • {ip} → {process}")
    else:
        print("❌ No external IPs found")
    
    print("\n🎯 Test completed!")

if __name__ == "__main__":
    main()
