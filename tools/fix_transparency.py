
from PyQt6.QtGui import QImage, QColor, QPixmap
from PyQt6.QtWidgets import QApplication
import sys
import os

def remove_green_bg():
    app = QApplication(sys.argv)
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_path = os.path.join(base_dir, 'assets', 'char.png')
    output_path = os.path.join(base_dir, 'assets', 'char_fixed.png')
    
    print(f"Loading: {input_path}")
    image = QImage(input_path)
    
    if image.isNull():
        print("Failed to load image!")
        return

    image = image.convertToFormat(QImage.Format.Format_ARGB32)
    
    width = image.width()
    height = image.height()
    
    # Target Green: 0, 255, 0
    # Tolerance
    limit = 100 # How far from green to be considered green
    
    for y in range(height):
        for x in range(width):
            pixel = image.pixelColor(x, y)
            
            # Simple distance check for Green
            # Bright green box is usually very pure
            r = pixel.red()
            g = pixel.green()
            b = pixel.blue()
            
            # Check if it's "Greenish"
            # High Green, Low Red/Blue
            if g > 200 and r < 100 and b < 100:
                # Set to transparent
                image.setPixelColor(x, y, QColor(0, 0, 0, 0))
                
    print(f"Saving to: {output_path}")
    image.save(output_path)
    print("Done.")

if __name__ == "__main__":
    remove_green_bg()
