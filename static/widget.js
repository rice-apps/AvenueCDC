document.addEventListener('DOMContentLoaded', () => {
    const chatLauncher = document.getElementById('chatLauncher');
    const chatWindow = document.getElementById('chatWindow');
    const closeChat = document.getElementById('closeChat');
    const chatBody = document.getElementById('chatBody');
    const languageRadios = document.querySelectorAll('input[name="language_select"]');
    const sendBtn = document.getElementById('sendBtn');

    // Same server that serves this page, so no host/port needed
    const API_URL = "";
    const MAIN_MENU_LABEL = { EN: "↩ Main menu", ES: "↩ Menú principal" };

    const getSelectedLang = () =>
        document.querySelector('input[name="language_select"]:checked').value.toUpperCase();

    // Open chat window; load the menu the first time
    chatLauncher.addEventListener('click', () => {
        chatWindow.style.display = 'flex';
        chatLauncher.style.display = 'none';
        if (chatBody.children.length <= 1) {
            loadMenuForSelectedLanguage();
        }
    });

    // Close chat window
    closeChat.addEventListener('click', () => {
        chatWindow.style.display = 'none';
        chatLauncher.style.display = 'flex';
    });

    // Reload the menu when the language changes
    languageRadios.forEach(radio => radio.addEventListener('change', () => {
        loadMenuForSelectedLanguage();
    }));

    sendBtn.addEventListener('click', () => {
        loadMenuForSelectedLanguage();
    });

    async function loadMenuForSelectedLanguage() {
        const selectedLang = getSelectedLang();
        try {
            const res = await fetch(`${API_URL}/initial?language=${selectedLang}`);
            const data = await res.json();
            chatBody.innerHTML = '';
            appendMessage(data.greeting, 'bot');
            renderOptionButtons(data.options);
        } catch (err) {
            appendMessage("Could not connect to back-end server.", 'bot');
        }
    }

    async function selectOption(optionText) {
        const selectedLang = getSelectedLang();
        appendMessage(optionText, 'user');
        clearOptionButtons();

        try {
            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: optionText, language: selectedLang })
            });
            const data = await response.json();

            if (data.status === "success") {
                appendMessage(data.reply, 'bot');
                if (data.options && data.options.length > 0) {
                    renderOptionButtons(data.options);
                } else {
                    // End of a branch: offer a way back instead of leaving the user stuck
                    renderOptionButtons([MAIN_MENU_LABEL[selectedLang]], loadMenuForSelectedLanguage);
                }
            } else {
                appendMessage("Sorry, I could not process that request.", 'bot');
            }
        } catch (error) {
            appendMessage("Error communicating with chatbot service.", 'bot');
        }
    }

    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = text;
        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function renderOptionButtons(options, onSelect = selectOption) {
        clearOptionButtons();
        const container = document.createElement('div');
        container.className = 'chat-options-container';
        container.style.cssText = "display: flex; flex-direction: column; gap: 8px; padding: 4px 12px; margin-top: 4px;";

        options.forEach(opt => {
            const btn = document.createElement('button');
            btn.className = 'chat-opt-btn';
            btn.textContent = opt;
            btn.style.cssText = "background: white; border: 1px solid #007bff; color: #007bff; padding: 10px 14px; border-radius: 18px; text-align: left; cursor: pointer; font-size: 13px; line-height: 1.3; transition: all 0.2s; font-family: inherit;";
            btn.addEventListener('mouseover', () => { btn.style.background = '#007bff'; btn.style.color = 'white'; });
            btn.addEventListener('mouseout', () => { btn.style.background = 'white'; btn.style.color = '#007bff'; });
            btn.addEventListener('click', () => onSelect(opt));

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
