"""
Network scanning utilities for finding external IP connections
"""
import subprocess
import ipaddress
import platform
from typing import Dict, Callable


class NetworkScanner:
    """Scans for external IP connections on the system"""
    
    def __init__(self):
        self.system = platform.system()
    
    def get_external_ips(self, log_callback: Callable[[str], None]) -> Dict[str, str]:
        """
        Get all external IP connections with their associated processes
        
        Args:
            log_callback: Function to call for logging messages
            
        Returns:
            Dictionary mapping IP addresses to process names
        """
        log_callback("🔍 Fetching all remote IP connections...")
        
        if self.system == "Windows":
            return self._get_external_ips_windows(log_callback)
        elif self.system in ["Linux", "Darwin"]:  # Darwin is macOS
            return self._get_external_ips_unix(log_callback)
        else:
            log_callback(f"❌ Unsupported operating system: {self.system}")
            return {}
    
    def _get_external_ips_windows(self, log_callback: Callable[[str], None]) -> Dict[str, str]:
        """Get external IPs on Windows using netstat"""
        try:
            result = subprocess.run(
                'netstat -ano',
                shell=True, capture_output=True, text=True, timeout=30
            )
            
            if result.returncode != 0:
                log_callback("❌ Failed to execute netstat command")
                return {}
            
            return self._parse_netstat_output(result.stdout, log_callback)
            
        except subprocess.TimeoutExpired:
            log_callback("❌ Netstat command timed out")
            return {}
        except Exception as e:
            log_callback(f"❌ Error running netstat: {str(e)}")
            return {}
    
    def _get_external_ips_unix(self, log_callback: Callable[[str], None]) -> Dict[str, str]:
        """Get external IPs on Unix-like systems using netstat or ss"""
        try:
            # Try ss first (more modern), then fallback to netstat
            # Use -tupn to show established connections with process info
            commands = [
                'ss -tupn state established',
                'netstat -tupn'
            ]
            
            for cmd in commands:
                try:
                    result = subprocess.run(
                        cmd, shell=True, capture_output=True, text=True, timeout=30
                    )
                    if result.returncode == 0:
                        return self._parse_unix_output(result.stdout, log_callback, cmd.startswith('ss'))
                except subprocess.TimeoutExpired:
                    continue
                except FileNotFoundError:
                    continue
            
            log_callback("❌ Neither ss nor netstat commands available")
            return {}
            
        except Exception as e:
            log_callback(f"❌ Error scanning network connections: {str(e)}")
            return {}
    
    def _parse_netstat_output(self, output: str, log_callback: Callable[[str], None]) -> Dict[str, str]:
        """Parse Windows netstat output"""
        ip_process_map = {}
        
        for line in output.splitlines():
            line = line.strip()
            if not line or line.startswith("Proto") or line.startswith("Active"):
                continue
            
            parts = line.split()
            if len(parts) < 5:
                continue
            
            try:
                foreign_addr = parts[2]
                pid = parts[-1]
                
                # Extract IP from address:port format
                if ":" not in foreign_addr:
                    continue
                
                raw_ip = foreign_addr.split(":")[0].strip("[]")
                
                # Validate and filter IP
                if not self._is_external_ip(raw_ip):
                    continue
                
                # Get process name
                proc_name = self._get_process_name_windows(pid)
                ip_process_map[raw_ip] = proc_name
                
            except (ValueError, IndexError):
                continue
        
        log_callback(f"🌐 Found {len(ip_process_map)} external IPs")
        return ip_process_map
    
    def _parse_unix_output(self, output: str, log_callback: Callable[[str], None], is_ss: bool = False) -> Dict[str, str]:
        """Parse Unix netstat/ss output"""
        ip_process_map = {}
        
        for line in output.splitlines():
            line = line.strip()
            if not line or line.startswith(("Proto", "Netid", "State", "Active")):
                continue
            
            parts = line.split()
            if len(parts) < 4:
                continue
            
            try:
                if is_ss:
                    # ss output format: Netid Recv-Q Send-Q Local_Address:Port Peer_Address:Port Process
                    if len(parts) < 5:
                        continue
                    
                    # When using 'ss -tupn state established', the state is already filtered
                    # so we don't need to check for "ESTAB" - all results are established
                    netid = parts[0]
                    if netid not in ["tcp", "udp"]:
                        continue
                    
                    foreign_addr = parts[4]
                    proc_name = self._extract_process_from_ss(parts[5:]) if len(parts) > 5 else "Unknown"
                    
                else:
                    # netstat output format: Proto Recv-Q Send-Q Local_Address Foreign_Address State [PID/Program]
                    if len(parts) < 5:
                        continue
                    
                    state = parts[5] if len(parts) > 5 else parts[4]
                    if "ESTABLISHED" not in state:
                        continue
                    
                    foreign_addr = parts[4]
                    proc_name = self._extract_process_from_netstat(parts[6:]) if len(parts) > 6 else "Unknown"
                
                # Extract IP from address:port format
                if ":" not in foreign_addr:
                    continue
                
                # Handle IPv6 addresses in brackets
                if foreign_addr.startswith('['):
                    # IPv6 format: [::1]:port
                    raw_ip = foreign_addr.split(']:')[0][1:]
                else:
                    # IPv4 format: ip:port
                    raw_ip = foreign_addr.rsplit(':', 1)[0]
                
                # Validate and filter IP
                if not self._is_external_ip(raw_ip):
                    continue
                
                ip_process_map[raw_ip] = proc_name
                
            except (ValueError, IndexError):
                continue
        
        log_callback(f"🌐 Found {len(ip_process_map)} external IPs")
        return ip_process_map
    
    def _is_external_ip(self, ip_str: str) -> bool:
        """Check if IP is external (not private, loopback, etc.)"""
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            return not (
                ip_obj.is_private or 
                ip_obj.is_loopback or 
                ip_obj.is_reserved or 
                ip_obj.is_link_local or 
                ip_obj.is_multicast
            )
        except ValueError:
            return False
    
    def _get_process_name_windows(self, pid: str) -> str:
        """Get process name from PID on Windows"""
        try:
            result = subprocess.run(
                f'tasklist /FI "PID eq {pid}"',
                shell=True, capture_output=True, text=True, timeout=10
            )
            
            for line in result.stdout.splitlines():
                if pid in line:
                    parts = line.split()
                    if parts:
                        return parts[0]
            
            return "Unknown"
            
        except Exception:
            return "Unknown"
    
    def _extract_process_from_ss(self, process_parts: list) -> str:
        """Extract process name from ss output"""
        if not process_parts:
            return "Unknown"
        
        # ss process format: users:(("process_name",pid=1234,fd=5))
        process_info = ' '.join(process_parts)
        
        try:
            if 'users:' in process_info:
                # Extract process name from users:(("name",pid=123,fd=4))
                start = process_info.find('(("') + 3
                end = process_info.find('",', start)
                if start > 2 and end > start:
                    return process_info[start:end]
            
            return "Unknown"
            
        except Exception:
            return "Unknown"
    
    def _extract_process_from_netstat(self, process_parts: list) -> str:
        """Extract process name from netstat output"""
        if not process_parts:
            return "Unknown"
        
        # netstat process format: PID/program_name
        process_info = ' '.join(process_parts)
        
        try:
            if '/' in process_info:
                return process_info.split('/')[-1]
            
            return "Unknown"
            
        except Exception:
            return "Unknown"
