
# QSS Styles for Joy AI Desktop

CHAT_BUBBLE_STYLE = """
QFrame {
    background-color: rgba(20, 20, 35, 240);
    border: 1px solid rgba(255, 255, 255, 30);
    border-radius: 15px;
}
"""

CHAT_INPUT_STYLE = """
QLineEdit {
    background-color: rgba(255, 255, 255, 20);
    border: 1px solid rgba(255, 255, 255, 50);
    border-radius: 10px;
    padding: 8px;
    color: white;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}
QLineEdit:focus {
    border: 1px solid #8e2de2;
    background-color: rgba(255, 255, 255, 30);
}
"""

MESSAGE_STYLE_USER = """
QLabel {
    background-color: #4a00e0;
    color: white;
    padding: 8px 12px;
    border-radius: 12px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}
"""

MESSAGE_STYLE_AI = """
QLabel {
    background-color: rgba(255, 255, 255, 30);
    color: white;
    padding: 8px 12px;
    border-radius: 12px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}
"""

CONTEXT_MENU_STYLE = """
QMenu {
    background-color: #2b2b2b;
    border: 1px solid #3d3d3d;
    color: white;
}
QMenu::item {
    background-color: transparent;
    padding: 8px 20px;
}
QMenu::item:selected {
    background-color: #4a00e0;
}
"""
