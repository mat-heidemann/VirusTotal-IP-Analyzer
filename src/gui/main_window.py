"""
Main GUI window for VirusTotal IP Analyzer
"""
import customtkinter as ctk
import threading
import webbrowser
import subprocess
import platform
from tkinter import filedialog
from typing import Dict, List, Callable, Optional
from src.core.config import DEFAULT_OUTPUT_PATH, DEFAULT_FIELDS, DEFAULT_BATCH_SIZE, DEFAULT_BATCH_DELAY, DEFAULT_MAX_IPS
from src.core.encryption import EncryptionManager
from src.core.scanner import IPScanner
from src.gui.api_key_dialog import APIKeyDialog
from src.gui.results_window import ResultsWindow
from src.gui.utils import force_dark_titlebar
from src.gui.custom_dialogs import show_error, show_info


class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.app = None
        self.scanner = None
        self.encryption_manager = EncryptionManager()
        self.current_scan_thread = None
        self._setup_gui()
    
    def _setup_gui(self):
        """Initialize the GUI"""
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.app = ctk.CTk()
        self.app.title("VirusTotal IP Analyzer")
        self.app.geometry("1280x700")
        self.app.minsize(850, 500)
        
        # Apply dark titlebar if on Windows
        if platform.system() == "Windows":
            self.app.after(100, lambda: force_dark_titlebar(self.app))
        
        self._create_widgets()
        self._update_api_indicator()
        
        # Handle window close
        self.app.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        main_frame = ctk.CTkFrame(self.app)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configuration section
        self._create_config_section(main_frame)
        
        # Log section
        self._create_log_section(main_frame)
    
    def _create_config_section(self, parent):
        """Create the configuration section"""
        config_section = ctk.CTkFrame(parent, corner_radius=10)
        config_section.pack(side="left", fill="y", padx=(0, 10), pady=10)
        
        ctk.CTkLabel(config_section, text="🔧 Configuration", font=("Arial", 14, "bold")).pack(
            anchor="w", pady=5, padx=10
        )
        
        # API Key controls
        self._create_api_controls(config_section)
        
        # Output path control
        self._create_output_controls(config_section)
        
        # Scan options
        self._create_scan_options(config_section)
        
        # Scan parameters
        self._create_scan_parameters(config_section)
        
        # Field selection
        self._create_field_selection(config_section)
        
        # Action buttons
        self._create_action_buttons(config_section)
    
    def _create_api_controls(self, parent):
        """Create API key controls"""
        top_controls = ctk.CTkFrame(parent, fg_color="transparent")
        top_controls.pack(fill="x", pady=(5, 10), padx=10)
        
        self.api_key_button = ctk.CTkButton(
            top_controls, 
            text="🔑 Set/Update API Key", 
            command=self._show_api_key_dialog
        )
        self.api_key_button.pack(fill="x", padx=5, pady=(5, 2))
        
        self.api_key_indicator = ctk.CTkLabel(
            top_controls, 
            text="🔴 No API Key", 
            text_color="red"
        )
        self.api_key_indicator.pack(fill="x", padx=5, pady=(0, 5))
    
    def _create_output_controls(self, parent):
        """Create output path controls"""
        self.output_path_var = ctk.StringVar(value=DEFAULT_OUTPUT_PATH)
        
        output_button = ctk.CTkButton(
            parent, 
            text="📁 Choose CSV Output", 
            command=self._choose_output_path
        )
        output_button.pack(fill="x", padx=10, pady=(2, 5))
    
    def _create_scan_options(self, parent):
        """Create scan option controls"""
        self.ignore_var = ctk.BooleanVar()
        
        ignore_frame = ctk.CTkFrame(parent, fg_color="transparent")
        ignore_frame.pack(fill="x", padx=10, pady=5)
        
        ignore_check = ctk.CTkCheckBox(
            ignore_frame, 
            text="Ignore already scanned IPs", 
            variable=self.ignore_var
        )
        ignore_check.pack(side="left")
        
        # Config folder button
        folder_icon = ctk.CTkLabel(ignore_frame, text="📂", cursor="hand2")
        folder_icon.pack(side="left", padx=(5, 0))
        folder_icon.bind("<Button-1>", lambda e: self._open_config_folder())
    
    def _create_scan_parameters(self, parent):
        """Create scan parameter controls"""
        inputs_frame = ctk.CTkFrame(parent, fg_color="transparent")
        inputs_frame.pack(fill="x", pady=5, padx=10)
        
        line = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        line.pack(fill="x", pady=5)
        
        # Max IPs
        ctk.CTkLabel(line, text="Max IPs:").pack(side="left")
        self.max_ips_entry = ctk.CTkEntry(line, width=50)
        self.max_ips_entry.insert(0, str(DEFAULT_MAX_IPS))
        self.max_ips_entry.pack(side="left", padx=5)
        
        # Batch Size
        ctk.CTkLabel(line, text="Batch Size:").pack(side="left", padx=(10, 0))
        self.batch_size_entry = ctk.CTkEntry(line, width=50)
        self.batch_size_entry.insert(0, str(DEFAULT_BATCH_SIZE))
        self.batch_size_entry.pack(side="left", padx=5)
        
        # Delay
        ctk.CTkLabel(line, text="Delay (s):").pack(side="left", padx=(10, 0))
        self.batch_delay_entry = ctk.CTkEntry(line, width=50)
        self.batch_delay_entry.insert(0, str(DEFAULT_BATCH_DELAY))
        self.batch_delay_entry.pack(side="left", padx=5)
    
    def _create_field_selection(self, parent):
        """Create field selection controls"""
        fields_section = ctk.CTkFrame(parent, corner_radius=10)
        fields_section.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            fields_section, 
            text="📋 Fields to export to CSV", 
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=5, padx=5)
        
        self.field_vars = {}
        for field in DEFAULT_FIELDS:
            var = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(fields_section, text=field, variable=var)
            cb.pack(anchor="w", padx=5, pady=2)
            self.field_vars[field] = var
    
    def _create_action_buttons(self, parent):
        """Create action buttons"""
        scan_buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        scan_buttons_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_button = ctk.CTkButton(
            scan_buttons_frame, 
            text="🚀 Start Scan", 
            corner_radius=10, 
            command=self._start_scan
        )
        self.start_button.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        show_results_button = ctk.CTkButton(
            scan_buttons_frame, 
            text="📊 Show Results", 
            corner_radius=10, 
            command=self._show_cached_results
        )
        show_results_button.pack(side="left", expand=True, fill="x", padx=(5, 0))
    
    def _create_log_section(self, parent):
        """Create the log section"""
        log_section = ctk.CTkFrame(parent, corner_radius=10)
        log_section.pack(side="right", fill="both", expand=True, padx=5, pady=10)
        
        ctk.CTkLabel(
            log_section, 
            text="📝 Scan Log:", 
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=5, padx=5)
        
        self.log_textbox = ctk.CTkTextbox(
            log_section, 
            wrap="word", 
            fg_color="#1e1e1e", 
            text_color="white"
        )
        self.log_textbox.pack(expand=True, fill="both", padx=10, pady=10)
        self.log_textbox.configure(state="disabled")
    
    def _show_api_key_dialog(self):
        """Show API key input dialog"""
        dialog = APIKeyDialog(self.app, self._update_api_indicator)
        dialog.show()
    
    def _choose_output_path(self):
        """Choose output CSV path"""
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if path:
            self.output_path_var.set(path)
    
    def _open_config_folder(self):
        """Open configuration folder"""
        from src.core.config import APPDATA_DIR
        
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.run(f'explorer "{APPDATA_DIR}"', shell=True)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", APPDATA_DIR])
            else:  # Linux
                subprocess.run(["xdg-open", APPDATA_DIR])
        except Exception as e:
            self.log(f"❌ Failed to open config folder: {str(e)}")
    
    def _update_api_indicator(self):
        """Update API key indicator"""
        if self.encryption_manager.is_api_key_defined():
            self.api_key_indicator.configure(text="✅ API Key Set", text_color="green")
        else:
            self.api_key_indicator.configure(text="🔴 No API Key", text_color="red")
    
    def _start_scan(self):
        """Start the scanning process"""
        if not self.encryption_manager.is_api_key_defined():
            show_error(self.app, "API Key Missing", "You must set your API Key before starting the scan.")
            return
        
        try:
            api_key = self.encryption_manager.load_api_key()
        except Exception as e:
            show_error(self.app, "Error", f"Failed to load API Key: {str(e)}")
            return
        
        # Validate parameters
        try:
            max_ips = int(self.max_ips_entry.get())
            batch_size = int(self.batch_size_entry.get())
            batch_delay = int(self.batch_delay_entry.get())
        except ValueError:
            show_error(self.app, "Error", "All scan parameters must be numeric.")
            return
        
        if batch_size <= 0:
            show_error(self.app, "Error", "Batch size must be greater than 0.")
            return
        
        # Get selected fields
        selected_fields = [f for f, v in self.field_vars.items() if v.get()]
        if not selected_fields:
            show_error(self.app, "Error", "You must select at least one field to export.")
            return
        
        # Start scan in separate thread
        self.scanner = IPScanner(api_key)
        self.current_scan_thread = threading.Thread(
            target=self._run_scan,
            args=(max_ips, batch_size, batch_delay, selected_fields)
        )
        self.current_scan_thread.start()
    
    def _run_scan(self, max_ips: int, batch_size: int, batch_delay: int, selected_fields: List[str]):
        """Run the scan in a separate thread"""
        try:
            self.start_button.configure(state="disabled", text="Scanning...")
            
            # Perform scan
            results = self.scanner.scan_network_ips(
                ignore_cache=self.ignore_var.get(),
                max_ips=max_ips,
                batch_size=batch_size,
                batch_delay=batch_delay,
                log_callback=self.log
            )
            
            if results:
                # Export to CSV
                self.scanner.export_to_csv(
                    results=results,
                    selected_fields=selected_fields,
                    csv_path=self.output_path_var.get(),
                    log_callback=self.log
                )
                
                # Show results window
                self.app.after(0, lambda: self._show_results_window(results))
            
        except Exception as e:
            self.log(f"❌ Scan failed: {str(e)}")
        finally:
            self.app.after(0, lambda: self.start_button.configure(state="normal", text="🚀 Start Scan"))
    
    def _show_results_window(self, results: List[Dict]):
        """Show results in a new window"""
        results_window = ResultsWindow(self.app, results)
        results_window.show()
    
    def _show_cached_results(self):
        """Show cached results"""
        from src.core.cache_manager import CacheManager
        
        cache_manager = CacheManager()
        cache = cache_manager.load_cache()
        
        if not cache:
            show_info(self.app, "No Results", "No previous scan results found.\n\nPlease run a scan first to generate results.")
            return
        
        results = list(cache.values())
        self._show_results_window(results)
    
    def log(self, message: str):
        """Add message to log"""
        def update_log():
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", f"{message}\n")
            self.log_textbox.see("end")
            self.log_textbox.configure(state="disabled")
        
        if threading.current_thread() != threading.main_thread():
            self.app.after(0, update_log)
        else:
            update_log()
    
    def _on_close(self):
        """Handle window close event"""
        # Stop any running scan
        if self.scanner:
            self.scanner.stop_scanning()
        
        # Clean up temp files
        from src.core.cache_manager import CacheManager
        cache_manager = CacheManager()
        cache_manager.clear_temp_results()
        
        self.app.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.app.mainloop()


class VirusTotalIPAnalyzer:
    """Wrapper class for backward compatibility"""
    
    def __init__(self):
        self.main_window = MainWindow()
    
    def run(self):
        """Start the GUI application"""
        self.main_window.run()
