
import ctypes
from ctypes import wintypes

def get_active_window_title():
    """
    Returns the title of the currently active window on Windows.
    Returns None if it fails.
    """
    try:
        user32 = ctypes.windll.user32
        h_wnd = user32.GetForegroundWindow()
        
        # Get title length
        length = user32.GetWindowTextLengthW(h_wnd)
        if length == 0:
            return None
            
        # Create buffer
        buff = ctypes.create_unicode_buffer(length + 1)
        
        # Get title
        user32.GetWindowTextW(h_wnd, buff, length + 1)
        
        return buff.value
    except Exception as e:
        print(f"Error getting window title: {e}")
        return None

if __name__ == "__main__":
    print(f"Active Window: {get_active_window_title()}")
