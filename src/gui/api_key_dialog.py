"""
API Key input dialog
"""
import customtkinter as ctk
import platform
from typing import Callable
from ..core.encryption import EncryptionManager
from .utils import force_dark_titlebar
from .custom_dialogs import show_error, show_warning, show_success


class APIKeyDialog:
    """Dialog for entering API key"""
    
    def __init__(self, parent, update_callback: Callable[[], None]):
        self.parent = parent
        self.update_callback = update_callback
        self.encryption_manager = EncryptionManager()
        self.popup = None
    
    def show(self):
        """Show the API key dialog"""
        self.popup = ctk.CTkToplevel(self.parent)
        self.popup.title("Set API Key")
        self.popup.geometry("400x200")
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.focus_force()
        self.popup.lift()
        
        # Delay grab_set to ensure window is visible
        self.popup.after(100, self.popup.grab_set)
        
        # Apply dark theme and titlebar
        ctk.set_appearance_mode("Dark")
        if platform.system() == "Windows":
            self.popup.after(100, lambda: force_dark_titlebar(self.popup))
        
        self._create_widgets()
        
        # Center the dialog
        self.popup.after(10, self.popup.lift)
    
    def _create_widgets(self):
        """Create dialog widgets"""
        # Title label
        label = ctk.CTkLabel(
            self.popup, 
            text="Enter your VirusTotal API Key:", 
            font=("Arial", 14)
        )
        label.pack(pady=(20, 10))
        
        # API key entry
        self.api_entry = ctk.CTkEntry(
            self.popup, 
            width=350, 
            placeholder_text="Paste your API key here",
            show=""  # Don't hide the text initially
        )
        self.api_entry.pack(pady=5)
        
        # Show/Hide button
        self.show_hide_button = ctk.CTkButton(
            self.popup,
            text="👁️ Hide",
            width=80,
            command=self._toggle_visibility
        )
        self.show_hide_button.pack(pady=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(self.popup, fg_color="transparent")
        button_frame.pack(pady=15)
        
        # Save button
        ok_button = ctk.CTkButton(
            button_frame, 
            text="Save", 
            command=self._save_key
        )
        ok_button.pack(side="left", padx=10)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            command=self._cancel
        )
        cancel_button.pack(side="left", padx=10)
        
        # Focus on entry
        self.api_entry.focus()
        
        # Bind Enter key to save
        self.popup.bind('<Return>', lambda e: self._save_key())
        self.popup.bind('<Escape>', lambda e: self._cancel())
    
    def _toggle_visibility(self):
        """Toggle API key visibility"""
        if self.api_entry.cget("show") == "":
            # Hide the text
            self.api_entry.configure(show="*")
            self.show_hide_button.configure(text="👁️ Show")
        else:
            # Show the text
            self.api_entry.configure(show="")
            self.show_hide_button.configure(text="👁️ Hide")
    
    def _save_key(self):
        """Save the API key"""
        key = self.api_entry.get().strip()
        
        if not key:
            show_error(self.popup, "Error", "API Key cannot be empty.")
            return
        
        # Basic validation - VirusTotal API keys are typically 64 characters
        if len(key) < 32:
            show_warning(
                self.popup,
                "Warning", 
                "API Key seems too short. Please verify it's correct."
            )
        
        try:
            self.encryption_manager.save_api_key(key)
            show_success(self.popup, "Success", "API Key saved successfully.")
            self.update_callback()
            self.popup.destroy()
        except Exception as e:
            show_error(self.popup, "Error", f"Failed to save API Key: {str(e)}")
    
    def _cancel(self):
        """Cancel the dialog"""
        self.popup.destroy()
