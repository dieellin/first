// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    // WebSocket connection
    let socket = null;
    let isStreaming = false;
    let currentAssistantMessage = null;
    
    // Connect WebSocket
    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/chat`;
        
        socket = new WebSocket(wsUrl);
        
        socket.onopen = function() {
            console.log('WebSocket connected');
        };
        
        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            
            if (data.error) {
                addMessage('system', `Error: ${data.error}`);
                isStreaming = false;
                return;
            }
            
            if (data.chunk) {
                if (!isStreaming) {
                    // Start a new assistant message
                    isStreaming = true;
                    currentAssistantMessage = document.createElement('div');
                    currentAssistantMessage.className = 'message assistant';
                    
                    const content = document.createElement('div');
                    content.className = 'message-content';
                    currentAssistantMessage.appendChild(content);
                    
                    messagesContainer.appendChild(currentAssistantMessage);
                }
                
                // Append to current message
                const content = currentAssistantMessage.querySelector('.message-content');
                content.textContent += data.chunk;
                
                // Scroll to bottom
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            if (data.done) {
                isStreaming = false;
                currentAssistantMessage = null;
                
                // Enable input after response is complete
                userInput.disabled = false;
                sendButton.disabled = false;
                userInput.focus();
            }
        };
        
        socket.onclose = function() {
            console.log('WebSocket disconnected. Reconnecting in 3 seconds...');
            setTimeout(connectWebSocket, 3000);
        };
        
        socket.onerror = function(error) {
            console.error('WebSocket error:', error);
        };
    }
    
    // Initialize WebSocket connection
    connectWebSocket();
    
    // Add a message to the chat
    function addMessage(role, text) {
        const message = document.createElement('div');
        message.className = `message ${role}`;
        
        const content = document.createElement('div');
        content.className = 'message-content';
        content.textContent = text;
        
        message.appendChild(content);
        messagesContainer.appendChild(message);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Send a message
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage('user', message);
        
        // Clear input
        userInput.value = '';
        
        // Disable input while waiting for response
        userInput.disabled = true;
        sendButton.disabled = true;
        
        // Send message via WebSocket
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ message }));
        } else {
            addMessage('system', 'WebSocket connection is not open. Reconnecting...');
            connectWebSocket();
            setTimeout(function() {
                if (socket && socket.readyState === WebSocket.OPEN) {
                    socket.send(JSON.stringify({ message }));
                } else {
                    addMessage('system', 'Failed to connect. Please try again later.');
                    userInput.disabled = false;
                    sendButton.disabled = false;
                }
            }, 1000);
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keydown', function(event) {
        // Send on Enter (without Shift)
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
    
    // Focus input on page load
    userInput.focus();
});
