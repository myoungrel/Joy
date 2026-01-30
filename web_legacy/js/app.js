import { ChatWidget } from './chat-widget.js';

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Chat Widget
    const joyAssistant = new ChatWidget();
    
    // Expose to window for debugging if needed
    window.joyAssistant = joyAssistant;
    
    console.log('Joy AI Assistant initialized 🚀');
});
