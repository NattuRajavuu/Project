const root = document.documentElement;
const themeToggle = document.querySelector('#theme-toggle');
const savedTheme = localStorage.getItem('luxe-theme') || 'light';
root.classList.toggle('dark', savedTheme === 'dark');

themeToggle?.addEventListener('click', () => {
  const next = root.classList.contains('dark') ? 'light' : 'dark';
  root.classList.toggle('dark', next === 'dark');
  localStorage.setItem('luxe-theme', next);
});

function setupChat(formId, inputId, messagesId, windowId = null) {
  const form = document.querySelector(formId);
  const input = document.querySelector(inputId);
  const messages = document.querySelector(messagesId);
  if (!form || !input || !messages) return;

  const append = (text, role) => {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${role}`;
    bubble.textContent = text;
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
    return bubble;
  };

  const send = async (text) => {
    if (!text.trim()) return;
    if (windowId) document.querySelector(windowId)?.classList.remove('hidden');
    append(text, 'user');
    input.value = '';
    const bot = append('Typing...', 'bot');

    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, provider: 'openai' }),
      });
      if (!response.ok || !response.body) throw new Error('Streaming unavailable');

      bot.textContent = '';
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const events = buffer.split('\n\n');
        buffer = events.pop() || '';
        events.forEach((event) => {
          const line = event.split('\n').find((item) => item.startsWith('data: '));
          if (!line) return;
          const payload = JSON.parse(line.slice(6));
          if (payload.type === 'token') bot.textContent += payload.content;
          messages.scrollTop = messages.scrollHeight;
        });
      }
      if (!bot.textContent.trim()) bot.textContent = 'I can help with products, shipping, returns, and checkout.';
    } catch {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, provider: 'openai' }),
      });
      const data = await response.json();
      bot.textContent = data.reply || 'I can help with products, shipping, returns, and checkout.';
    }
  };

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    send(input.value);
  });

  document.querySelectorAll('.suggestion').forEach((button) => {
    button.addEventListener('click', () => send(button.dataset.prompt || button.textContent));
  });
}

document.querySelector('#chat-toggle')?.addEventListener('click', () => {
  document.querySelector('#chat-window')?.classList.toggle('hidden');
  document.querySelector('#chat-input')?.focus();
});

document.querySelector('#chat-close')?.addEventListener('click', () => {
  document.querySelector('#chat-window')?.classList.add('hidden');
});

setupChat('#chat-form', '#chat-input', '#chat-messages', '#chat-window');
setupChat('#page-chat-form', '#page-chat-input', '#page-chat-messages');
