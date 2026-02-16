// Enhanced chat client with better UX
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('message-input');
  const messages = document.getElementById('messages');
  const loginBtn = document.getElementById('login-btn');
  const sendBtn = document.getElementById('send-btn');

  let isProcessing = false;

  // Quick action suggestions
  const quickActions = [
    "Create a meeting tomorrow at 2pm",
    "Delete my 3pm event today",
    "What's on my calendar?",
    "Schedule lunch next Monday at 12pm"
  ];

  function appendMessage(text, who = 'assistant') {
    const li = document.createElement('li');
    li.className = 'message ' + (who === 'user' ? 'user' : 'assistant');
    li.setAttribute('role', 'listitem');
    li.textContent = text;
    messages.appendChild(li);
    
    // Smooth scroll to bottom
    setTimeout(() => {
      li.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }, 100);
    
    return li;
  }

  function showTypingIndicator() {
    const li = document.createElement('li');
    li.className = 'message assistant typing-indicator';
    li.setAttribute('role', 'listitem');
    li.setAttribute('aria-label', 'Assistant is typing');
    li.innerHTML = '<span></span><span></span><span></span>';
    messages.appendChild(li);
    li.scrollIntoView({ behavior: 'smooth', block: 'end' });
    return li;
  }

  function removeTypingIndicator(indicator) {
    if (indicator && indicator.parentNode) {
      indicator.remove();
    }
  }

  function setProcessing(processing) {
    isProcessing = processing;
    sendBtn.disabled = processing;
    input.disabled = processing;
    
    if (processing) {
      sendBtn.querySelector('.btn-text').textContent = 'Sending...';
      sendBtn.style.opacity = '0.6';
    } else {
      sendBtn.querySelector('.btn-text').textContent = 'Send';
      sendBtn.style.opacity = '1';
    }
  }

  function addQuickActions() {
    // Check if quick actions already exist
    if (document.querySelector('.quick-actions')) return;
    
    const quickActionsDiv = document.createElement('div');
    quickActionsDiv.className = 'quick-actions';
    quickActionsDiv.innerHTML = '<small style="width: 100%; text-align: center; color: var(--text-muted); margin-bottom: 0.5rem;">💡 Try these:</small>';
    
    quickActions.forEach(action => {
      const btn = document.createElement('button');
      btn.className = 'quick-action';
      btn.textContent = action;
      btn.type = 'button';
      btn.onclick = () => {
        input.value = action;
        input.focus();
        form.requestSubmit();
      };
      quickActionsDiv.appendChild(btn);
    });
    
    form.parentNode.insertBefore(quickActionsDiv, form);
  }

  async function sendMessage(message) {
    if (isProcessing) return;
    
    appendMessage(message, 'user');
    setProcessing(true);
    
    const typingIndicator = showTypingIndicator();
    
    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      
      removeTypingIndicator(typingIndicator);
      
      if (res.status === 401) {
        loginBtn.style.display = 'inline-block';
        appendMessage('🔐 Please login with Google Calendar to manage events. You can still ask general questions!', 'assistant');
        return;
      }
      
      const data = await res.json();
      
      if (data.error) {
        appendMessage('❌ ' + (data.error || 'An error occurred'), 'assistant');
      } else if (data.response) {
        appendMessage(data.response, 'assistant');
      } else {
        appendMessage(JSON.stringify(data), 'assistant');
      }
    } catch (e) {
      removeTypingIndicator(typingIndicator);
      appendMessage('⚠️ Network error: ' + e.message, 'assistant');
    } finally {
      setProcessing(false);
    }
  }

  form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    const val = input.value.trim();
    if (!val || isProcessing) return;
    
    sendMessage(val);
    input.value = '';
    input.style.height = 'auto';
    input.focus();
  });

  // Auto-resize textarea
  input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = input.scrollHeight + 'px';
  });

  // Keyboard: Enter to send, Shift+Enter for newline
  input.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter' && !ev.shiftKey) {
      ev.preventDefault();
      form.requestSubmit();
    }
  });

  // Welcome message with delay for better UX
  setTimeout(() => {
    appendMessage('👋 Hi! I\'m your AI Calendar Assistant. I can help you:', 'assistant');
    setTimeout(() => {
      appendMessage('📅 Create calendar events\n🗑️ Delete events\n💬 Answer questions about your schedule\n\nTry asking me something!', 'assistant');
      addQuickActions();
    }, 800);
  }, 500);
});
