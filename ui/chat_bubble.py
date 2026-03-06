
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QFrame, QScrollArea, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QColor, QPainter, QPainterPath

from ui.styles import CHAT_BUBBLE_STYLE, CHAT_INPUT_STYLE, MESSAGE_STYLE_USER, MESSAGE_STYLE_AI

class ChatBubble(QWidget):
    message_sent = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Main Frame
        self.frame = QFrame()
        self.frame.setStyleSheet(CHAT_BUBBLE_STYLE)
        self.layout.addWidget(self.frame)
        
        self.frame_layout = QVBoxLayout(self.frame)
        
        # Message Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; } QWidget { background: transparent; }")
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.message_container = QWidget()
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.addStretch() # Push messages to bottom
        
        self.scroll_area.setWidget(self.message_container)
        self.frame_layout.addWidget(self.scroll_area)
        
        # Input Area
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Joy에게 물어보세요...")
        self.input_field.setStyleSheet(CHAT_INPUT_STYLE)
        self.input_field.returnPressed.connect(self.send_message)
        self.frame_layout.addWidget(self.input_field)
        
        # Initial Welcome Message
        self.add_message("안녕하세요! 무엇을 도와드릴까요? 😊", is_user=False)
        
        self.resize(300, 400)
    
    def send_message(self):
        text = self.input_field.text().strip()
        if text:
            self.add_message(text, is_user=True)
            self.message_sent.emit(text)
            self.input_field.clear()
            
    def add_message(self, text, is_user=True):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet(MESSAGE_STYLE_USER if is_user else MESSAGE_STYLE_AI)
        
        # Alignment
        h_layout = QHBoxLayout()
        if is_user:
            h_layout.addStretch()
            h_layout.addWidget(label)
        else:
            h_layout.addWidget(label)
            h_layout.addStretch()
            
        container = QWidget()
        container.setLayout(h_layout)
        self.message_layout.insertWidget(self.message_layout.count() - 1, container) # Insert before stretch
        
        # Auto scroll
        QTimer.singleShot(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
