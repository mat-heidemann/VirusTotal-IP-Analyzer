"""
Custom dialog boxes with consistent UI styling
"""
import customtkinter as ctk
import platform
from .utils import force_dark_titlebar


class CustomMessageBox:
    """Custom message box with consistent styling"""
    
    def __init__(self, parent, title: str, message: str, dialog_type: str = "info"):
        self.parent = parent
        self.title = title
        self.message = message
        self.dialog_type = dialog_type
        self.result = None
        self.popup = None
    
    def show(self) -> str:
        """Show the message box and return the result"""
        self.popup = ctk.CTkToplevel(self.parent)
        self.popup.title(self.title)
        
        # Adjust size based on dialog type and message length
        if self.dialog_type == "yesno" or len(self.message) > 100:
            self.popup.geometry("500x250")
        else:
            self.popup.geometry("400x200")
            
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.focus_force()
        self.popup.lift()
        
        # Center the dialog
        self.popup.geometry("+{}+{}".format(
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # Delay grab_set to ensure window is visible
        self.popup.after(100, self.popup.grab_set)
        
        # Apply dark theme and titlebar
        ctk.set_appearance_mode("Dark")
        if platform.system() == "Windows":
            self.popup.after(100, lambda: force_dark_titlebar(self.popup))
        
        self._create_widgets()
        
        # Wait for user response
        self.popup.wait_window()
        return self.result
    
    def _create_widgets(self):
        """Create dialog widgets"""
        # Icon and message frame
        content_frame = ctk.CTkFrame(self.popup, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icon
        icon_text = self._get_icon()
        icon_label = ctk.CTkLabel(
            content_frame,
            text=icon_text,
            font=("Arial", 24),
            width=50
        )
        icon_label.pack(pady=(0, 10))
        
        # Message
        message_label = ctk.CTkLabel(
            content_frame,
            text=self.message,
            font=("Arial", 12),
            wraplength=350,
            justify="center"
        )
        message_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(side="bottom")
        
        if self.dialog_type == "yesno":
            # Yes/No buttons
            yes_button = ctk.CTkButton(
                button_frame,
                text="Yes",
                command=self._yes_clicked,
                width=80
            )
            yes_button.pack(side="left", padx=5)
            
            no_button = ctk.CTkButton(
                button_frame,
                text="No",
                command=self._no_clicked,
                width=80
            )
            no_button.pack(side="left", padx=5)
        else:
            # OK button
            ok_button = ctk.CTkButton(
                button_frame,
                text="OK",
                command=self._ok_clicked,
                width=80
            )
            ok_button.pack()
        
        # Bind Enter and Escape keys
        self.popup.bind('<Return>', lambda e: self._ok_clicked())
        self.popup.bind('<Escape>', lambda e: self._ok_clicked())
    
    def _get_icon(self) -> str:
        """Get icon based on dialog type"""
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅",
            "question": "❓",
            "yesno": "❓"
        }
        return icons.get(self.dialog_type, "ℹ️")
    
    def _ok_clicked(self):
        """Handle OK button click"""
        self.result = "ok"
        self.popup.destroy()
    
    def _yes_clicked(self):
        """Handle Yes button click"""
        self.result = "yes"
        self.popup.destroy()
    
    def _no_clicked(self):
        """Handle No button click"""
        self.result = "no"
        self.popup.destroy()


def show_info(parent, title: str, message: str) -> str:
    """Show info message box"""
    dialog = CustomMessageBox(parent, title, message, "info")
    return dialog.show()


def show_warning(parent, title: str, message: str) -> str:
    """Show warning message box"""
    dialog = CustomMessageBox(parent, title, message, "warning")
    return dialog.show()


def show_error(parent, title: str, message: str) -> str:
    """Show error message box"""
    dialog = CustomMessageBox(parent, title, message, "error")
    return dialog.show()


def show_success(parent, title: str, message: str) -> str:
    """Show success message box"""
    dialog = CustomMessageBox(parent, title, message, "success")
    return dialog.show()


def show_question(parent, title: str, message: str) -> str:
    """Show yes/no question dialog"""
    dialog = CustomMessageBox(parent, title, message, "yesno")
    return dialog.show()
