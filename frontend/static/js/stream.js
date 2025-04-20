// Stream Handling
document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('chat-messages');
    
    // Process text with markdown and code formatting
    function processText(text) {
        // Handle code blocks
        text = text.replace(/```(\w+)?\n([\s\S]*?)```/g, function(match, language, code) {
            language = language || '';
            return `<pre><code class="language-${language}">${escapeHtml(code.trim())}</code></pre>`;
        });
        
        // Handle inline code
        text = text.replace(/`([^`]+)`/g, function(match, code) {
            return `<code>${escapeHtml(code)}</code>`;
        });
        
        // Handle line breaks
        text = text.replace(/\n/g, '<br>');
        
        return text;
    }
    
    // Escape HTML special characters
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    
    // Function to update message content with formatted text
    function updateMessageContent(message, text) {
        const content = message.querySelector('.message-content');
        content.innerHTML = processText(text);
    }
    
    // Observer to watch for new messages and format them
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && node.classList.contains('message')) {
                        const content = node.querySelector('.message-content');
                        if (content) {
                            const text = content.textContent;
                            content.innerHTML = processText(text);
                        }
                    }
                });
            }
        });
    });
    
    // Start observing the chat messages container
    observer.observe(messagesContainer, { childList: true });
    
    // Create and show typing indicator
    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'message assistant typing-indicator';
        indicator.innerHTML = `
            <div class="message-content">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        messagesContainer.appendChild(indicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return indicator;
    }
    
    // Remove typing indicator
    function removeTypingIndicator(indicator) {
        if (indicator && indicator.parentNode) {
            indicator.parentNode.removeChild(indicator);
        }
    }
    
    // Expose functions to window for use in chat.js
    window.chatUtils = {
        showTypingIndicator,
        removeTypingIndicator,
        updateMessageContent,
        processText
    };
});
