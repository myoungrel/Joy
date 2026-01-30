import aiService from './ai-service.js';

/**
 * Chat Widget Component
 * Handles all UI interactions for the chat interface
 */
export class ChatWidget {
    constructor() {
        this.cacheDOM();
        this.isOpen = false;
        this.messageHistory = [];
        this.init();
        this.loadChatHistory();
    }
    
    cacheDOM() {
        this.chatWidget = document.getElementById('chatWidget');
        this.chatToggleBtn = document.getElementById('chatToggleBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.minimizeBtn = document.getElementById('minimizeBtn');
        this.closeBtn = document.getElementById('closeBtn');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.notificationBadge = document.getElementById('notificationBadge');
        this.quickActionBtns = document.querySelectorAll('.quick-action-btn');
    }
    
    init() {
        // Event listeners
        this.chatToggleBtn.addEventListener('click', () => this.toggleChat());
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.minimizeBtn.addEventListener('click', () => this.minimizeChat());
        this.closeBtn.addEventListener('click', () => this.closeChat());
        
        // Input handling
        this.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        this.chatInput.addEventListener('input', () => {
            this.chatInput.style.height = 'auto';
            this.chatInput.style.height = this.chatInput.scrollHeight + 'px';
        });
        
        // Quick action buttons
        this.quickActionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const message = btn.getAttribute('data-message');
                this.chatInput.value = message;
                this.chatInput.focus();
            });
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.minimizeChat();
            }
        });
        
        // Show welcome notification after 2 seconds
        setTimeout(() => {
            if (!this.isOpen) {
                this.showNotification();
            }
        }, 2000);
    }
    
    toggleChat() {
        if (this.isOpen) {
            this.minimizeChat();
        } else {
            this.openChat();
        }
    }
    
    openChat() {
        this.isOpen = true;
        this.chatWidget.classList.add('active');
        this.chatWidget.classList.remove('minimized');
        this.chatToggleBtn.classList.add('hidden');
        this.hideNotification();
        this.chatInput.focus();
        this.scrollToBottom();
    }
    
    minimizeChat() {
        this.isOpen = false;
        this.chatWidget.classList.remove('active');
        this.chatWidget.classList.add('minimized');
        this.chatToggleBtn.classList.remove('hidden');
    }
    
    closeChat() {
        this.minimizeChat();
    }
    
    sendMessage() {
        const message = this.chatInput.value.trim();
        
        if (!message) return;
        
        // Add user message
        this.addMessage(message, 'user');
        
        // Clear input
        this.chatInput.value = '';
        this.chatInput.style.height = 'auto';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Get AI response
        setTimeout(() => {
            this.hideTypingIndicator();
            const response = aiService.generateResponse(message);
            this.addMessage(response, 'ai');
        }, 1000 + Math.random() * 1000);
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = sender === 'ai' ? 'J' : 'U';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        // Support multiple paragraphs
        const paragraphs = text.split('\n').filter(p => p.trim());
        paragraphs.forEach(p => {
            const para = document.createElement('p');
            para.textContent = p;
            content.appendChild(para);
        });
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Save to history
        this.messageHistory.push({ text, sender, timestamp: Date.now() });
        this.saveChatHistory();
    }
    
    showTypingIndicator() {
        this.typingIndicator.classList.remove('hidden');
    }
    
    hideTypingIndicator() {
        this.typingIndicator.classList.add('hidden');
    }
    
    showNotification() {
        this.notificationBadge.classList.remove('hidden');
    }
    
    hideNotification() {
        this.notificationBadge.classList.add('hidden');
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    saveChatHistory() {
        try {
            localStorage.setItem('joyAssistantHistory', JSON.stringify(this.messageHistory));
        } catch (e) {
            console.warn('Failed to save chat history:', e);
        }
    }
    
    loadChatHistory() {
        try {
            const saved = localStorage.getItem('joyAssistantHistory');
            if (saved) {
                this.messageHistory = JSON.parse(saved);
                
                // Restore messages (limit to last 20)
                const recentMessages = this.messageHistory.slice(-20);
                
                // Clear existing messages except welcome message
                const welcomeMessage = this.chatMessages.querySelector('.message');
                this.chatMessages.innerHTML = '';
                if (welcomeMessage) {
                    this.chatMessages.appendChild(welcomeMessage);
                }
                
                // Add saved messages
                recentMessages.forEach(msg => {
                    // Check if message already exists (simple check)
                    const existingText = this.chatMessages.innerText;
                    if (!existingText.includes(msg.text)) {
                         this.addMessageWithoutSave(msg.text, msg.sender);
                    }
                });
            }
        } catch (e) {
            console.warn('Failed to load chat history:', e);
        }
    }
    
    addMessageWithoutSave(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = sender === 'ai' ? 'J' : 'U';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const paragraphs = text.split('\n').filter(p => p.trim());
        paragraphs.forEach(p => {
            const para = document.createElement('p');
            para.textContent = p;
            content.appendChild(para);
        });
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        this.chatMessages.appendChild(messageDiv);
    }
}
