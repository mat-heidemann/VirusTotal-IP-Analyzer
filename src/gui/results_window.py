"""
Results display window for showing scan results
"""
import customtkinter as ctk
import webbrowser
import subprocess
import platform
from typing import Dict, List, Set
from .utils import force_dark_titlebar
from .custom_dialogs import show_info, show_error, show_question
from ..core.ip_blocker import IPBlocker


class ResultsWindow:
    """Window for displaying scan results"""
    
    def __init__(self, parent, results: List[Dict]):
        self.parent = parent
        self.results = results
        self.window = None
        self.selected_entry_frame = None
        self.ip_blocker = IPBlocker()
        self.show_cached = ctk.BooleanVar(value=False)
        self.filter_negative_reputation = ctk.BooleanVar(value=False)
        
        # UI components
        self.details_title = None
        self.details_content = None
        self.block_button = None
        self.unblock_button = None
        self.vt_button = None
        self.abuse_button = None
        self.ip_list_title = None
        self.ip_buttons_frame = None
    
    def show(self):
        """Show the results window"""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Scanned IPs")
        self.window.geometry("1150x800")
        self.window.transient(self.parent)
        self.window.focus_force()
        self.window.lift()
        
        # Delay grab_set to ensure window is visible
        self.window.after(100, self.window.grab_set)
        
        # Apply dark theme and titlebar
        ctk.set_appearance_mode("Dark")
        if platform.system() == "Windows":
            self.window.after(100, lambda: force_dark_titlebar(self.window))
        
        self._create_widgets()
        self._refresh_list()
    
    def _create_widgets(self):
        """Create all window widgets"""
        # Toggle frame
        toggle_frame = ctk.CTkFrame(self.window)
        toggle_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        ctk.CTkCheckBox(
            toggle_frame, 
            text="Show previously scanned IPs (cache)", 
            variable=self.show_cached, 
            command=self._refresh_list
        ).pack(anchor="w")
        
        ctk.CTkCheckBox(
            toggle_frame, 
            text="🔴 Filter IPs with reputation score < 0 (malicious)", 
            variable=self.filter_negative_reputation, 
            command=self._refresh_list
        ).pack(anchor="w", pady=(5, 0))
        
        # Main split frame
        split_frame = ctk.CTkFrame(self.window, corner_radius=10)
        split_frame.pack(expand=True, fill="both", padx=15, pady=10)
        split_frame.grid_rowconfigure(0, weight=1)
        split_frame.grid_columnconfigure(0, weight=2)
        split_frame.grid_columnconfigure(1, weight=1)
        
        # IP list frame
        self._create_ip_list_frame(split_frame)
        
        # Details frame
        self._create_details_frame(split_frame)
    
    def _create_ip_list_frame(self, parent):
        """Create the IP list frame"""
        ip_list_frame = ctk.CTkFrame(parent, corner_radius=10)
        ip_list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)
        
        self.ip_list_title = ctk.CTkLabel(
            ip_list_frame, 
            text="🌐 IPs Found", 
            font=("Arial", 14, "bold")
        )
        self.ip_list_title.pack(anchor="w", pady=5, padx=10)
        
        self.ip_buttons_frame = ctk.CTkScrollableFrame(ip_list_frame, corner_radius=10)
        self.ip_buttons_frame.pack(expand=True, fill="both", padx=8, pady=8)
    
    def _create_details_frame(self, parent):
        """Create the details frame"""
        details_frame = ctk.CTkFrame(parent, corner_radius=10)
        details_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=8)
        
        self.details_title = ctk.CTkLabel(
            details_frame, 
            text="ℹ️ Select an IP to view details", 
            font=("Arial", 14, "bold")
        )
        self.details_title.pack(anchor="w", pady=8, padx=10)
        
        self.details_content = ctk.CTkTextbox(
            details_frame, 
            wrap="word", 
            fg_color="#1E1E1E", 
            text_color="white", 
            font=("Consolas", 12), 
            border_width=0, 
            corner_radius=8
        )
        self.details_content.pack(expand=True, fill="both", padx=10, pady=(0, 8))
        self.details_content.configure(state="disabled")
        
        # Action buttons
        self._create_action_buttons(details_frame)
    
    def _create_action_buttons(self, parent):
        """Create action buttons"""
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(pady=8)
        
        self.block_button = ctk.CTkButton(
            buttons_frame, 
            text="⛔ Block IP", 
            width=120, 
            state="disabled"
        )
        self.block_button.pack(side="left", padx=5)
        
        self.vt_button = ctk.CTkButton(
            buttons_frame, 
            text="🔎 VirusTotal", 
            width=120, 
            state="disabled"
        )
        self.vt_button.pack(side="left", padx=5)
        
        self.abuse_button = ctk.CTkButton(
            buttons_frame, 
            text="🚨 AbuseIPDB", 
            width=120, 
            state="disabled"
        )
        self.abuse_button.pack(side="left", padx=5)
    
    def _refresh_list(self):
        """Refresh the IP list"""
        try:
            if self.show_cached.get():
                # Load from cache
                from ..core.cache_manager import CacheManager
                cache_manager = CacheManager()
                cache = cache_manager.load_cache()
                full_list = list(cache.values()) if cache else []
            else:
                # Use current results
                full_list = self.results
        except Exception as e:
            print(f"Error loading results: {e}")
            full_list = []
        
        self.ip_list_title.configure(text=f"🌐 IPs Found ({len(full_list)})")
        
        # Clear existing widgets
        for widget in self.ip_buttons_frame.winfo_children():
            widget.destroy()
        
        # Apply reputation filter if enabled
        if self.filter_negative_reputation.get():
            filtered_list = []
            for entry in full_list:
                reputation_score = entry.get("Reputation Score", "N/A")
                if isinstance(reputation_score, int) and reputation_score < 0:
                    filtered_list.append(entry)
            full_list = filtered_list
            
            # Update title to show filtered count
            self.ip_list_title.configure(text=f"🔴 Malicious IPs Found ({len(full_list)})")
        
        # Create IP entries
        for entry in sorted(full_list, key=lambda x: x.get("IP", "")):
            self._create_ip_entry(entry)
    
    def _create_ip_entry(self, entry: Dict):
        """Create an IP entry widget"""
        ip = entry.get("IP", "")
        process_name = entry.get("Process Name", "Unknown")
        reputation_score = entry.get("Reputation Score", "N/A")
        
        # Get engine stats
        malicious = entry.get("Engines Malicious", 0)
        suspicious = entry.get("Engines Suspicious", 0)
        harmless = entry.get("Engines Harmless", 0)
        
        # Get community votes
        malicious_votes = entry.get("Community Malicious Votes", 0)
        harmless_votes = entry.get("Community Harmless Votes", 0)
        
        # Check if IP is blocked for visual feedback
        is_blocked = self.ip_blocker.is_blocked(ip)
        
        # Create entry frame with different color if blocked
        frame_color = "#4a1a1a" if is_blocked else "#2E2E2E"  # Dark red tint if blocked
        entry_frame = ctk.CTkFrame(self.ip_buttons_frame, corner_radius=8, fg_color=frame_color)
        entry_frame.pack(fill="x", padx=5, pady=6)
        
        # Header with IP and reputation
        header_frame = ctk.CTkFrame(entry_frame, fg_color="transparent")
        header_frame.pack(anchor="w", fill="x", padx=8, pady=(4, 4))
        
        # IP label with blocked indicator
        ip_text = f"{ip} ({process_name})"
        if is_blocked:
            ip_text = f"🚫 {ip_text} [BLOCKED]"
        
        ctk.CTkLabel(
            header_frame, 
            text=ip_text, 
            anchor="w", 
            font=("Arial", 12, "bold"), 
            text_color="#ff6b6b" if is_blocked else "white"
        ).pack(side="left")
        
        # Reputation score box
        rep_color = "#5cb85c" if isinstance(reputation_score, int) and reputation_score >= 0 else "#d9534f"
        rep_box = ctk.CTkFrame(header_frame, width=120, height=30, corner_radius=6, fg_color=rep_color)
        rep_box.pack(side="right", padx=6)
        rep_box.pack_propagate(False)
        
        ctk.CTkLabel(
            rep_box, 
            text=f"Score: {reputation_score}", 
            font=("Arial", 12, "bold"), 
            text_color="white"
        ).pack(expand=True)
        
        # Engine analysis
        engines_text = "Most engines consider it harmless"
        engines_color = "#5cb85c" if (malicious + suspicious) <= harmless else "#d9534f"
        if engines_color == "#d9534f":
            engines_text = "Most engines consider it malicious/suspicious"
        
        # Community votes
        votes_text = "Community voted as harmless"
        votes_color = "#5cb85c" if malicious_votes <= harmless_votes else "#d9534f"
        if votes_color == "#d9534f":
            votes_text = "Community voted as malicious"
        
        # Info container
        info_container = ctk.CTkFrame(entry_frame, fg_color="transparent")
        info_container.pack(anchor="w", padx=12, pady=(0, 6))
        
        # Engines line
        engines_line = ctk.CTkFrame(info_container, fg_color="transparent")
        engines_line.pack(anchor="w")
        
        circle1 = ctk.CTkFrame(engines_line, width=10, height=10, fg_color=engines_color, corner_radius=5)
        circle1.pack(side="left", padx=(0, 6), pady=2)
        
        ctk.CTkLabel(
            engines_line, 
            text=engines_text, 
            font=("Arial", 11), 
            text_color="white"
        ).pack(side="left")
        
        # Votes line
        votes_line = ctk.CTkFrame(info_container, fg_color="transparent")
        votes_line.pack(anchor="w", pady=(2, 0))
        
        circle2 = ctk.CTkFrame(votes_line, width=10, height=10, fg_color=votes_color, corner_radius=5)
        circle2.pack(side="left", padx=(0, 6), pady=2)
        
        ctk.CTkLabel(
            votes_line, 
            text=votes_text, 
            font=("Arial", 11), 
            text_color="white"
        ).pack(side="left")
        
        # Bind click event
        self._bind_recursive(entry_frame, lambda e, en=entry, ef=entry_frame: self._show_details(en, ef))
    
    def _bind_recursive(self, widget, func):
        """Recursively bind click event to widget and children"""
        widget.bind("<Button-1>", func)
        for child in widget.winfo_children():
            self._bind_recursive(child, func)
    
    def _show_details(self, entry: Dict, entry_frame):
        """Show details for selected IP"""
        ip = entry.get("IP", "")
        process_name = entry.get("Process Name", "Unknown")
        
        # Update title
        self.details_title.configure(text=f"ℹ️ {ip} ({process_name})")
        
        # Update content
        self.details_content.configure(state="normal")
        self.details_content.delete("1.0", "end")
        
        # Basic info
        self.details_content.insert("end", f"Reputation Score: {entry.get('Reputation Score', 'N/A')}\n")
        self.details_content.insert("end", f"Country: {entry.get('Country', 'N/A')}\n")
        self.details_content.insert("end", f"ASN: {entry.get('ASN', 'N/A')}\n")
        self.details_content.insert("end", f"ASN Owner: {entry.get('ASN Owner', 'N/A')}\n")
        self.details_content.insert("end", f"Last Analysis Date: {entry.get('Last Analysis Date', 'N/A')}\n\n")
        
        # Engine stats
        self.details_content.insert("end", f"Engines Malicious: {entry.get('Engines Malicious', 0)}\n")
        self.details_content.insert("end", f"Engines Suspicious: {entry.get('Engines Suspicious', 0)}\n")
        self.details_content.insert("end", f"Engines Harmless: {entry.get('Engines Harmless', 0)}\n")
        self.details_content.insert("end", f"Community Malicious Votes: {entry.get('Community Malicious Votes', 0)}\n")
        self.details_content.insert("end", f"Community Harmless Votes: {entry.get('Community Harmless Votes', 0)}\n\n")
        
        # Antivirus engines
        self.details_content.insert("end", "Antivirus Engines:\n")
        for engine, result in entry.get("Analysis Results", {}).items():
            self.details_content.insert("end", f"  {engine}: {result}\n")
        
        self.details_content.configure(state="disabled")
        
        # Update selection
        if self.selected_entry_frame and self.selected_entry_frame.winfo_exists():
            self.selected_entry_frame.configure(fg_color="#2E2E2E")
        entry_frame.configure(fg_color="#1E3A8A")
        self.selected_entry_frame = entry_frame
        
        # Update buttons based on blocking status
        is_blocked = self.ip_blocker.is_blocked(ip)
        if is_blocked:
            self.block_button.configure(
                text="🔓 Unblock IP",
                state="normal",
                fg_color="#f39c12",
                hover_color="#e67e22",
                command=lambda: self._unblock_ip(ip)
            )
        else:
            self.block_button.configure(
                text="⛔ Block IP",
                state="normal",
                fg_color="#e74c3c",
                hover_color="#c0392b",
                command=lambda: self._block_ip(ip)
            )
        self.vt_button.configure(
            state="normal",
            command=lambda: webbrowser.open(f"https://www.virustotal.com/gui/ip-address/{ip}")
        )
        self.abuse_button.configure(
            state="normal",
            command=lambda: webbrowser.open(f"https://www.abuseipdb.com/check/{ip}")
        )
    
    def _block_ip(self, ip: str):
        """Block an IP address using the IP blocker"""
        result = show_question(
            self.window,
            "Confirm Block",
            f"Do you really want to block the IP?\n{ip}\n\nThis will add firewall rules to block all traffic to/from this IP."
        )
        
        if result == "yes":
            success, message = self.ip_blocker.block_ip(ip)
            if success:
                show_info(self.window, "Success", message)
                # Update button state
                self._update_button_for_ip(ip)
                # Refresh the list to show visual changes
                self._refresh_list()
            else:
                show_error(self.window, "Error", message)
    
    def _unblock_ip(self, ip: str):
        """Unblock an IP address using the IP blocker"""
        result = show_question(
            self.window,
            "Confirm Unblock",
            f"Do you want to unblock the IP?\n{ip}\n\nThis will remove firewall rules blocking this IP."
        )
        
        if result == "yes":
            success, message = self.ip_blocker.unblock_ip(ip)
            if success:
                show_info(self.window, "Success", message)
                # Update button state
                self._update_button_for_ip(ip)
                # Refresh the list to show visual changes
                self._refresh_list()
            else:
                show_error(self.window, "Error", message)
    
    def _update_button_for_ip(self, ip: str):
        """Update button state for a specific IP"""
        is_blocked = self.ip_blocker.is_blocked(ip)
        if is_blocked:
            self.block_button.configure(
                text="🔓 Unblock IP",
                fg_color="#f39c12",
                hover_color="#e67e22",
                command=lambda: self._unblock_ip(ip)
            )
        else:
            self.block_button.configure(
                text="⛔ Block IP",
                fg_color="#e74c3c",
                hover_color="#c0392b",
                command=lambda: self._block_ip(ip)
            )
