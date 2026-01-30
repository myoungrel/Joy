import sys
import os
import math
import traceback
from PyQt6.QtWidgets import QWidget, QLabel, QApplication, QMenu, QSystemTrayIcon
from PyQt6.QtCore import Qt, QPoint, QTimer, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QAction, QIcon, QPainter, QCursor, QRegion, QBitmap, QColor, QPainterPath, QImage

from ui.chat_bubble import ChatBubble
from ui.styles import CONTEXT_MENU_STYLE
# Import the new AI Worker
# Note: Since we are running from main.py, core is accessible
try:
    from core.ai import AIWorker
    from core.context import get_active_window_title
    from core.vision import capture_active_window_base64
except ImportError:
    pass # Add manual handling later if needed
    class AIWorker(QThread):
        response_ready = pyqtSignal(str)
        def __init__(self, *args, **kwargs): super().__init__()
        def run(self): self.response_ready.emit("AI Core Module Missing! (Check dependencies)")

class JoyWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # State variables
        self.dragging = False
        self.offset = QPoint()
        self.follow_mouse = False
        self.auto_vision_mode = False # Default: Off
        self.setWindowTitle("Joy Assistant")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Start Context Tracker
        self.start_context_tracking()
        
        # Assets Path
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        
        # UI Setup (Initialize first)
        self.target_size = 120
        self.label = QLabel(self)
        self.resize(self.target_size, self.target_size)
        
        # Load and Process All Character States
        self.states = {}
        self.load_state('idle', 'char.png')
        self.load_state('thinking', 'char_thinking.png')
        self.load_state('speaking', 'char_speaking.png')
        self.load_state('happy', 'char_happy.png')
        
        # Set Initial State
        self.set_state('idle')
        
        # Apply mask 
        self.apply_circular_mask()
        
        
        # Initial Position (Bottom Right)
        screen = QApplication.primaryScreen().geometry()
        self.target_pos = QPoint(screen.width() - self.width() - 50, screen.height() - self.height() - 80)
        self.move(self.target_pos)
        
        # Chat Bubble
        self.chat_bubble = ChatBubble()
        self.chat_bubble.hide()
        self.chat_bubble.message_sent.connect(self.handle_ai_response)
        
        # Breathing Animation
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.breathing_animation)
        self.anim_timer.start(50)
        self.anim_step = 0
        
        # Speaking Animation Timer (Revert to idle)
        self.speaking_timer = QTimer(self)
        self.speaking_timer.setSingleShot(True)
        self.speaking_timer.timeout.connect(lambda: self.set_state('idle'))
        
        # Context Menu & Tray
        self.init_context_menu()
        self.init_tray_icon()

    def load_state(self, state_name, filename):
        path = os.path.join(self.assets_dir, filename)
        if not os.path.exists(path):
            print(f"Warning: Asset {filename} not found, using char.png")
            path = os.path.join(self.assets_dir, 'char.png')
            
        original = QPixmap(path)
        if original.isNull():
            # Create placeholder
            original = QPixmap(120, 120)
            original.fill(Qt.GlobalColor.green)
            
        # Process Green Screen immediately
        processed = self.process_green_screen(original)
        self.states[state_name] = processed

    def process_green_screen(self, pixmap):
        # 1. Scale image
        scaled = pixmap.scaled(
            self.target_size, self.target_size, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        
        # 2. Process Image for "Green Screen" Transparency
        image = scaled.toImage()
        image = image.convertToFormat(QImage.Format.Format_ARGB32)
        
        width = image.width()
        height = image.height()
        
        for y in range(height):
            for x in range(width):
                pixel = image.pixelColor(x, y)
                r, g, b = pixel.red(), pixel.green(), pixel.blue()
                
                # Green Screen Detection
                is_green = (g > 80) and (g > r + 30) and (g > b + 30)
                is_bright_green = (g > 200) and (r < 150) and (b < 150)
                
                if is_green or is_bright_green:
                    image.setPixelColor(x, y, QColor(0, 0, 0, 0)) 
                    
        return QPixmap.fromImage(image)

    def set_state(self, state_name):
        if state_name in self.states:
            self.pixmap = self.states[state_name]
            self.label.setPixmap(self.pixmap)
            if not self.pixmap.isNull():
                 self.setMask(self.pixmap.mask())

    def update_pixmap(self):
        # Deprecated: logic moved to load_state/process_green_screen
        pass

    def apply_circular_mask(self):
        pass

    def init_context_menu(self):
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def show_context_menu(self, pos):
        # DEBUG LOGGING
        with open("debug_menu.txt", "w") as f: f.write("Menu Requested")
        
        try:
            menu = QMenu(self)
            # menu.setStyleSheet(CONTEXT_MENU_STYLE) # Temporarily disable style
            
            # --- Essential Features Only ---
            
            # 1. Vision Features
            vision_action = QAction("👀 현재 화면 보고 대답하기", self)
            vision_action.triggered.connect(self.trigger_vision_chat)
            menu.addAction(vision_action)
            
            auto_vision_action = QAction("✅ 대화할 때마다 화면 보기 (Auto)", self)
            auto_vision_action.setCheckable(True)
            auto_vision_action.setChecked(getattr(self, 'auto_vision_mode', False))
            auto_vision_action.triggered.connect(self.toggle_auto_vision)
            menu.addAction(auto_vision_action)
            
            menu.addSeparator()
            
            # 2. Utility Features
            reset_action = QAction("원위치로 이동", self)
            reset_action.triggered.connect(self.reset_position)
            menu.addAction(reset_action)
            
            quit_action = QAction("종료", self)
            quit_action.triggered.connect(QApplication.instance().quit)
            menu.addAction(quit_action)
            
            menu.exec(self.mapToGlobal(pos))
        except Exception as e:
            error_msg = traceback.format_exc()
            with open("crash_log.txt", "w", encoding="utf-8") as f:
                f.write(error_msg)
            print(f"CRASH: {error_msg}")

    def init_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.path.join(self.assets_dir, 'char.png'))) # Use a default icon
        
        tray_menu = QMenu()
        show_action = QAction("보이기/숨기기", self)
        show_action.triggered.connect(self.toggle_visibility)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("종료", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def toggle_follow(self, checked):
        self.follow_mouse = checked

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
            self.chat_bubble.hide()
        else:
            self.show()

    def reset_position(self):
        screen = QApplication.primaryScreen().geometry()
        self.target_pos = QPoint(screen.width() - self.width() - 50, screen.height() - self.height() - 80)
        self.move(self.target_pos)
        self.current_pos = self.target_pos

    def track_mouse(self): pass

    def breathing_animation(self):
        if self.dragging: return
        self.anim_step += 0.05
        # Breathing affects Y only
        self.breathing_offset = math.sin(self.anim_step) * 2
        self.update_animation_pos()

    def update_animation_pos(self):
        # Only breathing (Y)
        breath_y = getattr(self, 'breathing_offset', 0)
        
        # Move the label inside the widget
        self.label.move(0, int(breath_y))

    # Mouse Events
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.position().toPoint()
            self.drag_start_pos = event.position().toPoint() # Track start pos to distinguish click vs drag
            # Temporarily disable follow while dragging
            self.anim_timer.stop() 

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            new_pos = self.mapToGlobal(event.position().toPoint()) - self.offset
            self.move(new_pos)
            self.current_pos = new_pos # Update current pos to avoid jump when releasing
            if self.chat_bubble.isVisible():
                self.update_chat_position()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.anim_timer.start(50)
        
        # Only process click if Left Button was released
        if event.button() == Qt.MouseButton.LeftButton:
            # Safe check in case drag_start_pos wasn't set (e.g. if press event was missed)
            if not hasattr(self, 'drag_start_pos'):
                return
                
            # Check if it was a click (not a drag)
            # We check distance moved
            current_pos = event.position().toPoint()
            dist = (current_pos - self.drag_start_pos).manhattanLength()
            
            if dist < 3: # Threshold for click
                if self.chat_bubble.isVisible():
                    self.chat_bubble.hide()
                else:
                    self.show_chat_bubble()

    def show_chat_bubble(self):
        self.update_chat_position()
        self.chat_bubble.show()
        self.chat_bubble.raise_()
        self.chat_bubble.activateWindow()
        self.chat_bubble.input_field.setFocus()
        
        # Greet happily if first opening?
        # self.set_state('happy')
        # QTimer.singleShot(2000, lambda: self.set_state('idle'))

    def update_chat_position(self):
        geo = self.geometry()
        bubble_geo = self.chat_bubble.geometry()
        
        # Default: Top-Left relative to character
        x = geo.x() - bubble_geo.width() - 10
        y = geo.y() - bubble_geo.height() + geo.height() // 2
        
        # Boundary checks
        if x < 0: x = geo.x() + geo.width() + 10
        if y < 0: y = 20
        
        self.chat_bubble.move(x, y)


    # Context Tracking
    def start_context_tracking(self):
        self.last_valid_context = "Unknown"
        self.context_timer = QTimer(self)
        self.context_timer.timeout.connect(self.track_context)
        self.context_timer.start(500) # Check every 0.5s
        
    def track_context(self):
        current = get_active_window_title()
        if current:
            # Ignore our own windows
            # We set window title to "Joy Assistant" in __init__
            if "Joy Assistant" not in current and "python" not in current.lower():
                self.last_valid_context = current
                # print(f"DEBUG: Tracked Context: {self.last_valid_context}")

    # Vision Logic
    def trigger_vision_chat(self):
        # 1. Capture Screen
        print("DEBUG: Capturing Screen...")
        image_data = capture_active_window_base64()
        
        if not image_data:
            self.show_chat_bubble()
            self.chat_bubble.add_message("화면을 캡처하지 못했어요. 😢", is_user=False)
            return

        # 2. Show bubble and ask what to look for
        self.show_chat_bubble()
        self.chat_bubble.input_field.setPlaceholderText("화면을 보고 무엇을 알려드릴까요?")
        self.chat_bubble.add_message("👀 화면을 보고 있어요! 무엇이 궁금하신가요?", is_user=False)
        
        # 3. Store valid image temporarily to attach to next message
        self.pending_image = image_data

    def toggle_auto_vision(self, checked):
        self.auto_vision_mode = checked
        mode_text = "켜짐" if checked else "꺼짐"
        print(f"DEBUG: Auto Vision Mode {mode_text}")
        
    # AI Logic
    def handle_ai_response(self, user_text):
        print(f"DEBUG: Handling AI Response for: {user_text}")
        
        # 0. Get Context
        context = getattr(self, 'last_valid_context', "Unknown")
        
        # 0.5. Check for pending image OR Auto Vision
        image_data = getattr(self, 'pending_image', None)
        
        # Auto Vision Logic: Capture if mode is on and no manual image exists
        if not image_data and self.auto_vision_mode:
            print("DEBUG: Auto-Capturing Screen for Vision Request")
            image_data = capture_active_window_base64()
            
        if image_data:
            print("DEBUG: Attaching Screen Image to request")
            self.pending_image = None # Consume it
        
        # 1. Start Thinking
        self.set_state('thinking')
        
        # Create worker
        self.worker = AIWorker(user_text, context_info=context, image_data=image_data)
        self.worker.response_ready.connect(self.on_ai_response)
        self.worker.start()
        
    def on_ai_response(self, response_text):
        print(f"DEBUG: AI Response received: {response_text[:20]}...")
        # 2. Speaking/Happy when done
        print("DEBUG: Setting state to SPEAKING")
        self.set_state('speaking')
        self.chat_bubble.add_message(response_text, is_user=False)
        
        # 3. Revert to Idle after a few seconds
        duration = min(max(len(response_text) * 100, 2000), 5000)
        self.speaking_timer.start(duration)


