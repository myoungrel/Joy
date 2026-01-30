
import os
import sys

# Add joy_libs to path
libs_path = os.path.join(os.path.dirname(__file__), 'joy_libs')
sys.path.append(libs_path)

from PIL import Image

def remove_green_screen(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        r, g, b, a = item
        # Simple Green Screen Logic (matching widget.py's approximate thresholds)
        # is_green = (g > 80) and (g > r + 30) and (g > b + 30)
        # is_bright_green = (g > 200) and (r < 150) and (b < 150)
        
        if (g > 80 and g > r + 30 and g > b + 30) or (g > 200 and r < 150 and b < 150):
            new_data.append((255, 255, 255, 0)) # Transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Saved clean image to {output_path}")

if __name__ == "__main__":
    remove_green_screen("assets/char.png", "assets/joy_preview.png")
