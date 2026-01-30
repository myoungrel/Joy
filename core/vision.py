
import base64
from io import BytesIO
from PIL import Image, ImageGrab

def capture_active_window_base64():
    """
    Captures the entire screen (simplification for active window context)
    and returns it as a base64 encoded string.
    """
    try:
        # Capture full screen using Pillow (No extra dependency like pyautogui needed)
        screenshot = ImageGrab.grab()
        
        # Resize for performance (Ollama doesn't need 4K images)
        screenshot.thumbnail((1024, 1024))
        
        buffered = BytesIO()
        screenshot.save(buffered, format="JPEG", quality=80)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return img_str
    except Exception as e:
        print(f"Vision Error: {e}")
        return None

if __name__ == "__main__":
    # Test
    b64 = capture_active_window_base64()
    print(f"Captured Base64 Length: {len(b64) if b64 else 'None'}")
