
import sys
import os

# Add local library path (joy_libs) to sys.path
# This allows running the app without installing libs globally
current_dir = os.path.dirname(os.path.abspath(__file__))
libs_dir = os.path.join(current_dir, 'joy_libs')
if os.path.exists(libs_dir):
    sys.path.insert(0, libs_dir)

# Ensure project root is in sys.path
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from PyQt6.QtWidgets import QApplication
from ui.widget import JoyWidget

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # Keep app running in tray
    
    joy = JoyWidget()
    joy.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
