document.addEventListener('DOMContentLoaded', () => {
    const chatLauncher = document.getElementById('chatLauncher');
    const chatWindow = document.getElementById('chatWindow');
    const closeChat = document.getElementById('closeChat');
    const chatBody = document.getElementById('chatBody');
    const sendBtn = document.getElementById('sendBtn');
    
    const API_URL = "http://127.0.0.1:5050";

    chatLauncher.addEventListener('click', () => {
        chatWindow.style.display = 'flex';
        chatLauncher.style.display = 'none';
    });

    closeChat.addEventListener('click', () => {
        chatWindow.style.display = 'none';
        chatLauncher.style.display = 'flex';
    });

    // Submits the selected radio button choice to FastAPI
    sendBtn.addEventListener('click', async () => {
        const selectedRadio = document.querySelector('input[name="language_select"]:checked');
        if (!selectedRadio) return;

        const langValue = selectedRadio.value.toUpperCase(); // 'EN' or 'ES'

        try {
            // 1. Submit language configuration update to FastAPI endpoint
            const response = await fetch(`${API_URL}/submit-chatbot_language`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ language_select: langValue.toLowerCase() })
            });
            
            if (response.ok) {
                // 2. Fetch the actual conversational starting menu list from python
                const menuRes = await fetch(`${API_URL}/api/initial?language=${langValue}`);
                const data = await menuRes.json();
                
                chatBody.innerHTML = `<div class="message bot">${data.greeting}</div>`;
                renderOptionButtons(data.options);
            }
        } catch (error) {
            appendMessage("Could not connect to backend server.", "bot");
        }
    });

    async function selectOption(optionText) {
        const selectedRadio = document.querySelector('input[name="language_select"]:checked');
        const currentLang = selectedRadio ? selectedRadio.value.toUpperCase() : "EN";

        appendMessage(optionText, 'user');
        clearOptionButtons();

        try {
            const response = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: optionText, language: currentLang })
            });
            const data = await response.json();

            if (data.status === "success") {
                appendMessage(data.reply, 'bot');

                if (data.options && data.options.length > 0) {
                    renderOptionButtons(data.options);
                }
            }
        } catch (err) {
            appendMessage("Error communicating with chatbot logic script.", "bot");
        }
    }

    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function renderOptionButtons(options) {
        clearOptionButtons();

        const container = document.createElement('div');
        container.className = 'chat-options-container';
        container.style.cssText = "display: flex; flex-direction: column; gap: 8px; padding: 4px 12px; margin-top: 4px;";

        options.forEach(opt => {
            const btn = document.createElement('button');
            btn.textContent = opt;
            btn.style.cssText = "background: white; border: 1px solid #007bff; color: #007bff; padding: 10px 14px; border-radius: 18px; text-align: left; cursor: pointer; font-size: 13px; line-height: 1.3; transition: all 0.2s; font-family: inherit;";
            
            btn.addEventListener('mouseover', () => { btn.style.background = '#007bff'; btn.style.color = 'white'; });
            btn.addEventListener('mouseout', () => { btn.style.background = 'white'; btn.style.color = '#007bff'; });
            btn.addEventListener('click', () => selectOption(opt));
            
            container.appendChild(btn);
        });

        chatBody.appendChild(container);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function clearOptionButtons() {
        const existing = document.querySelector('.chat-options-container');
        if (existing) existing.remove();
    }
});

