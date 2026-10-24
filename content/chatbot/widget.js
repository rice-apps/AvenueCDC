document.addEventListener('DOMContentLoaded', () => {
    const chatLauncher = document.getElementById('chatLauncher');
    const chatWindow = document.getElementById('chatWindow');
    const closeChat = document.getElementById('closeChat');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatBody = document.getElementById('chatBody');

    // Toggle chat window open
    chatLauncher.addEventListener('click', () => {
        chatWindow.style.display = 'flex';
        chatLauncher.style.display = 'none';
        chatInput.focus();
    });

    // Toggle chat window close
    closeChat.addEventListener('click', () => {
        chatWindow.style.display = 'none';
        chatLauncher.style.display = 'flex';
    });

    // Handle user action to send message
    function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Append User Message
        appendMessage(text, 'user');
        chatInput.value = '';

        // Simulate Bot Response (Replace this with your API call)
        setTimeout(() => {
            appendMessage("I received your message! (Connect your backend API here).", 'bot');
        }, 1000);
    }

    // Generate and inject message bubbles into DOM
    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = text;
        chatBody.appendChild(messageDiv);
        
        // Auto scroll to bottom
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Hook listeners up to events
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
