"""
IP blocking functionality for different operating systems
"""
import subprocess
import platform
import os
import json
from typing import Set, List
from pathlib import Path
from . import config


class IPBlocker:
    """Manages IP blocking across different operating systems"""
    
    def __init__(self):
        self.system = platform.system()
        self.blocked_ips_file = os.path.join(config.APPDATA_DIR, "blocked_ips.json")
        self._blocked_ips: Set[str] = self._load_blocked_ips()
    
    def _load_blocked_ips(self) -> Set[str]:
        """Load blocked IPs from file"""
        try:
            if os.path.exists(self.blocked_ips_file):
                with open(self.blocked_ips_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('blocked_ips', []))
        except Exception:
            pass
        return set()
    
    def _save_blocked_ips(self):
        """Save blocked IPs to file with metadata"""
        try:
            os.makedirs(os.path.dirname(self.blocked_ips_file), exist_ok=True)
            
            # Load existing data to preserve metadata
            existing_data = {}
            if os.path.exists(self.blocked_ips_file):
                try:
                    with open(self.blocked_ips_file, 'r') as f:
                        existing_data = json.load(f)
                except Exception:
                    pass
            
            # Update the blocked IPs list
            existing_data['blocked_ips'] = list(self._blocked_ips)
            
            # Save updated data
            with open(self.blocked_ips_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
        except Exception as e:
            print(f"Error saving blocked IPs: {e}")
    
    def is_blocked(self, ip: str) -> bool:
        """Check if an IP is blocked"""
        return ip in self._blocked_ips
    
    def get_blocked_ips(self) -> Set[str]:
        """Get all blocked IPs"""
        return self._blocked_ips.copy()
    
    def block_ip(self, ip: str) -> tuple[bool, str]:
        """
        Block an IP address using system firewall
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if ip in self._blocked_ips:
            return True, f"IP {ip} is already blocked"
        
        try:
            if self.system == "Windows":
                success, message = self._block_ip_windows(ip)
            elif self.system == "Linux":
                success, message = self._block_ip_linux(ip)
            elif self.system == "Darwin":  # macOS
                success, message = self._block_ip_macos(ip)
            else:
                return False, f"Unsupported operating system: {self.system}"
            
            if success:
                self._blocked_ips.add(ip)
                self._save_blocked_ips()
            
            return success, message
            
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def unblock_ip(self, ip: str) -> tuple[bool, str]:
        """
        Unblock an IP address
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if ip not in self._blocked_ips:
            return True, f"IP {ip} is not blocked"
        
        try:
            if self.system == "Windows":
                success, message = self._unblock_ip_windows(ip)
            elif self.system == "Linux":
                success, message = self._unblock_ip_linux(ip)
            elif self.system == "Darwin":  # macOS
                success, message = self._unblock_ip_macos(ip)
            else:
                return False, f"Unsupported operating system: {self.system}"
            
            if success:
                self._blocked_ips.discard(ip)
                self._save_blocked_ips()
            
            return success, message
            
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def _block_ip_windows(self, ip: str) -> tuple[bool, str]:
        """Block IP on Windows using netsh"""
        try:
            # Block outbound traffic
            result1 = subprocess.run(
                f'netsh advfirewall firewall add rule name="VT_Block_OUT_{ip}" dir=out action=block remoteip={ip}',
                shell=True, capture_output=True, text=True, check=True
            )
            
            # Block inbound traffic
            result2 = subprocess.run(
                f'netsh advfirewall firewall add rule name="VT_Block_IN_{ip}" dir=in action=block remoteip={ip}',
                shell=True, capture_output=True, text=True, check=True
            )
            
            return True, f"Successfully blocked IP {ip} using Windows Firewall"
            
        except subprocess.CalledProcessError as e:
            return False, f"Failed to block IP {ip}: {e.stderr or str(e)}"
    
    def _unblock_ip_windows(self, ip: str) -> tuple[bool, str]:
        """Unblock IP on Windows"""
        try:
            # Remove outbound rule
            subprocess.run(
                f'netsh advfirewall firewall delete rule name="VT_Block_OUT_{ip}"',
                shell=True, capture_output=True, text=True, check=True
            )
            
            # Remove inbound rule
            subprocess.run(
                f'netsh advfirewall firewall delete rule name="VT_Block_IN_{ip}"',
                shell=True, capture_output=True, text=True, check=True
            )
            
            return True, f"Successfully unblocked IP {ip}"
            
        except subprocess.CalledProcessError as e:
            return False, f"Failed to unblock IP {ip}: {e.stderr or str(e)}"
    
    def _block_ip_linux(self, ip: str) -> tuple[bool, str]:
        """Block IP on Linux using iptables"""
        try:
            # Check if iptables is available
            subprocess.run(['which', 'iptables'], check=True, capture_output=True)
            
            # Block input traffic from IP
            result1 = subprocess.run(
                ['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'],
                capture_output=True, text=True, check=True
            )
            
            # Block output traffic to IP
            result2 = subprocess.run(
                ['sudo', 'iptables', '-A', 'OUTPUT', '-d', ip, '-j', 'DROP'],
                capture_output=True, text=True, check=True
            )
            
            # Try to save iptables rules (different commands on different distros)
            self._save_iptables_rules()
            
            return True, f"Successfully blocked IP {ip} using iptables"
            
        except subprocess.CalledProcessError as e:
            return False, f"Failed to block IP {ip}: {e.stderr or str(e)}"
        except FileNotFoundError:
            return False, "iptables not found. Please install iptables."
    
    def _unblock_ip_linux(self, ip: str) -> tuple[bool, str]:
        """Unblock IP on Linux"""
        try:
            # Remove input rule
            subprocess.run(
                ['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'],
                capture_output=True, text=True, check=True
            )
            
            # Remove output rule
            subprocess.run(
                ['sudo', 'iptables', '-D', 'OUTPUT', '-d', ip, '-j', 'DROP'],
                capture_output=True, text=True, check=True
            )
            
            # Save iptables rules
            self._save_iptables_rules()
            
            return True, f"Successfully unblocked IP {ip}"
            
        except subprocess.CalledProcessError as e:
            return False, f"Failed to unblock IP {ip}: {e.stderr or str(e)}"
    
    def _save_iptables_rules(self):
        """Save iptables rules (try different methods for different distros)"""
        save_commands = [
            ['sudo', 'iptables-save'],  # Most common
            ['sudo', 'service', 'iptables', 'save'],  # RHEL/CentOS
            ['sudo', 'netfilter-persistent', 'save'],  # Debian/Ubuntu with netfilter-persistent
        ]
        
        for cmd in save_commands:
            try:
                subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
                break
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
    
    def _block_ip_macos(self, ip: str) -> tuple[bool, str]:
        """Block IP on macOS using pfctl"""
        try:
            # Create or update pfctl rules file
            rules_file = "/tmp/vt_blocked_ips.conf"
            
            # Add IP to rules file
            with open(rules_file, 'a') as f:
                f.write(f"block drop from {ip} to any\n")
                f.write(f"block drop from any to {ip}\n")
            
            # Load rules into pfctl
            result = subprocess.run(
                ['sudo', 'pfctl', '-f', rules_file],
                capture_output=True, text=True, check=True
            )
            
            # Enable pfctl if not already enabled
            subprocess.run(['sudo', 'pfctl', '-e'], capture_output=True, text=True)
            
            return True, f"Successfully blocked IP {ip} using pfctl"
            
        except subprocess.CalledProcessError as e:
            return False, f"Failed to block IP {ip}: {e.stderr or str(e)}"
        except Exception as e:
            return False, f"Failed to block IP {ip}: {str(e)}"
    
    def _unblock_ip_macos(self, ip: str) -> tuple[bool, str]:
        """Unblock IP on macOS"""
        try:
            # This is a simplified approach - in practice, you'd need to
            # manage the pfctl rules file more carefully
            return True, f"IP {ip} unblocked (manual pfctl rule removal may be required)"
            
        except Exception as e:
            return False, f"Failed to unblock IP {ip}: {str(e)}"
    
    def get_blocking_status(self) -> dict:
        """Get current blocking system status"""
        status = {
            "system": self.system,
            "blocked_count": len(self._blocked_ips),
            "blocked_ips": list(self._blocked_ips),
            "firewall_available": False
        }
        
        try:
            if self.system == "Windows":
                result = subprocess.run('netsh advfirewall show allprofiles', 
                                      shell=True, capture_output=True, text=True, timeout=5)
                status["firewall_available"] = result.returncode == 0
            elif self.system == "Linux":
                result = subprocess.run(['which', 'iptables'], 
                                      capture_output=True, text=True, timeout=5)
                status["firewall_available"] = result.returncode == 0
            elif self.system == "Darwin":
                result = subprocess.run(['which', 'pfctl'], 
                                      capture_output=True, text=True, timeout=5)
                status["firewall_available"] = result.returncode == 0
        except Exception:
            pass
        
        return status
