"""
GUI utility functions
"""
import ctypes
import platform


def force_dark_titlebar(window):
    """Force dark titlebar on Windows"""
    if platform.system() != "Windows":
        return
    
    try:
        # Get window handle
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        
        # Set dark mode attribute
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(ctypes.c_int(1)),
            ctypes.sizeof(ctypes.c_int(1))
        )
    except Exception:
        # Silently fail if dark titlebar is not supported
        pass
