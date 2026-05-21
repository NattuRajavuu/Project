import { useEffect, useMemo, useRef, useState } from 'react';
import { Loader2, MessageSquare, Mic, Send, Trash2, X } from 'lucide-react';
import { products } from '../data/products';
import { useCart } from '../context/CartContext';

const STORAGE_KEY = 'luxe-chatbot-history';
const LANGUAGES = [
  { value: 'en', label: 'English' },
  { value: 'es', label: 'Español' },
];

const defaultHistory = [
  {
    id: 'welcome',
    role: 'assistant',
    text: 'Welcome to Luxe Chat. I can help you with products, orders, shipping, returns, and your cart.',
  },
];

const sanitize = (value) => String(value || '').replace(/<|>/g, '');

const summarizeCart = (cart, totals) => {
  if (!cart.length) return 'Your cart is empty. Add a product by asking me to add one.';
  return `You have ${cart.length} item(s) in your cart with a subtotal of $${totals.subtotal.toFixed(2)} and total $${totals.total.toFixed(2)}.`;
};

const findProduct = (message) => {
  const query = message.toLowerCase();
  return products.find((product) => product.name.toLowerCase().includes(query) || product.id.toLowerCase().includes(query));
};

const localFallback = (message) => {
  const normalized = message.toLowerCase();
  if (/shipping|delivery|arrive/.test(normalized)) {
    return 'Shipping is free for orders over $100 and typically arrives in 3-5 business days. Need faster delivery? Just ask.';
  }
  if (/refund|return|cancel/.test(normalized)) {
    return 'Refunds are processed within 5-7 business days after approval. Share your order ID when you are ready and I will help you with the next steps.';
  }
  if (/payment|card|apple pay|google pay/.test(normalized)) {
    return 'We accept credit cards, debit cards, Apple Pay, Google Pay, and secure local checkout methods.';
  }
  if (/warranty|guarantee/.test(normalized)) {
    return 'All items include a one-year limited warranty covering manufacturing defects and quality issues.';
  }
  if (/order.*track|tracking|order status/.test(normalized)) {
    return 'Send me your order ID and I can check the status from the local order database.';
  }
  if (/recommend|find|suggest|best|show me/.test(normalized)) {
    return 'Tell me a product category or price range, and I will suggest items that match your preference.';
  }
  return 'I am here to help with products, shipping, orders, cart updates, and FAQs. Try asking about a product name or order status.';
};

export default function Chatbot() {
  const { cart, addToCart, removeFromCart, totals } = useCart();
  const [open, setOpen] = useState(false);
  const [history, setHistory] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : defaultHistory;
    } catch {
      return defaultHistory;
    }
  });
  const [text, setText] = useState('');
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const containerRef = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history]);

  useEffect(() => {
    if (!open) return;
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [open]);

  const openChat = () => setOpen(true);

  const appendMessage = (message) => {
    setHistory((prev) => [...prev, message]);
  };

  const clearHistory = () => {
    setHistory(defaultHistory);
    localStorage.removeItem(STORAGE_KEY);
  };

  const handleCartCommand = (message) => {
    const match = message.toLowerCase().match(/(?:add|remove)\s+(?:the\s+)?(.+)/);
    const summary = /cart|summary|what.*in.*cart/.test(message.toLowerCase());
    if (summary) {
      return { response: summarizeCart(cart, totals), intent: 'cart_summary' };
    }
    if (!match) return null;
    const query = match[1];
    const product = findProduct(query);
    if (!product) return { response: `I could not find a product matching "${query}". Try a different name.`, intent: 'cart_missing' };
    if (message.toLowerCase().startsWith('remove')) {
      removeFromCart(product.id);
      return { response: `${product.name} has been removed from your cart.`, intent: 'cart_remove' };
    }
    addToCart(product, 1);
    return { response: `${product.name} has been added to your cart.`, intent: 'cart_add' };
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const cleaned = sanitize(text).trim();
    if (!cleaned) return;
    const userMessage = { id: `user-${Date.now()}`, role: 'user', text: cleaned };
    appendMessage(userMessage);
    setText('');
    setLoading(true);

    const cartResult = handleCartCommand(cleaned);
    if (cartResult) {
      appendMessage({ id: `bot-${Date.now()}`, role: 'assistant', text: cartResult.response });
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: cleaned, language }),
      });
      if (!response.ok) throw new Error('API unavailable');
      const data = await response.json();
      appendMessage({
        id: `bot-${Date.now()}`,
        role: 'assistant',
        text: data.reply || data.response || localFallback(cleaned),
        products: data.products || [],
      });
    } catch (error) {
      appendMessage({ id: `bot-${Date.now()}`, role: 'assistant', text: localFallback(cleaned) });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!voiceEnabled) return undefined;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return undefined;

    const recognition = new SpeechRecognition();
    recognition.lang = language;
    recognition.interimResults = true;
    recognition.continuous = true;

    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0].transcript)
        .join('');
      setText(transcript);
    };
    recognition.onerror = () => {
      setVoiceEnabled(false);
    };
    recognition.start();

    return () => recognition.stop();
  }, [voiceEnabled, language]);

  const recommendedProducts = useMemo(() => {
    const shopperQuery = history
      .slice()
      .reverse()
      .find((entry) => entry.role === 'user' && /recommend|find|suggest|best/.test(entry.text.toLowerCase()));
    if (!shopperQuery) return [];
    return products.filter((product) => shopperQuery.text.toLowerCase().includes(product.category.toLowerCase())).slice(0, 3);
  }, [history]);

  return (
    <div ref={containerRef} className="fixed bottom-6 right-6 z-50 flex flex-col items-end sm:bottom-8 sm:right-8">
      {!open && (
        <button
          className="group inline-flex h-14 w-14 items-center justify-center rounded-full bg-ink text-white shadow-xl transition hover:scale-[1.03]"
          onClick={openChat}
          aria-label="Open chatbot"
        >
          <MessageSquare className="h-6 w-6" />
        </button>
      )}
      {open && (
        <div className="glass w-[340px] max-w-[90vw] overflow-hidden rounded-[32px] border border-black/10 shadow-2xl dark:border-white/10">
          <div className="flex items-center justify-between border-b border-black/10 px-4 py-4 dark:border-white/10">
            <div>
              <p className="text-sm font-semibold">Luxe Chat Assistant</p>
              <p className="text-[13px] text-slate-500 dark:text-slate-300">Fast offline support for products, orders, and checkout.</p>
            </div>
            <button className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/90 text-ink transition hover:bg-white" onClick={() => setOpen(false)} aria-label="Close chat">
              <X className="h-4 w-4" />
            </button>
          </div>
          <div className="flex flex-col gap-2 p-4">
            <div className="flex items-center justify-between gap-2 rounded-3xl bg-black/5 p-3 text-xs text-slate-600 dark:bg-white/10 dark:text-slate-300">
              <span>Language</span>
              <select className="rounded-2xl border border-black/10 bg-white/80 px-2 py-1 text-sm outline-none dark:border-white/10 dark:bg-white/10" value={language} onChange={(event) => setLanguage(event.target.value)}>
                {LANGUAGES.map((lang) => (
                  <option key={lang.value} value={lang.value}>{lang.label}</option>
                ))}
              </select>
            </div>
            <div className="max-h-72 space-y-3 overflow-y-auto px-1 pb-2">
              {history.map((message) => (
                <div key={message.id} className={`rounded-3xl p-3 ${message.role === 'assistant' ? 'bg-white text-ink shadow-sm dark:bg-white/10 dark:text-white' : 'bg-ink text-white dark:bg-slate-800'}`}>
                  <p className="text-sm whitespace-pre-wrap">{message.text}</p>
                  {message.products?.length > 0 && (
                    <div className="mt-3 grid gap-2">
                      {message.products.map((product) => (
                        <div key={product.id} className="rounded-3xl border border-black/10 bg-slate-50 p-3 dark:border-white/10 dark:bg-slate-900">
                          <p className="font-semibold">{product.name}</p>
                          <p className="text-xs text-slate-500 dark:text-slate-400">{product.category}</p>
                          <p className="mt-2 text-sm">${product.price.toFixed(2)} · {product.tag}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
            {recommendedProducts.length > 0 && (
              <div className="rounded-3xl border border-black/10 bg-slate-50 p-3 text-sm dark:border-white/10 dark:bg-slate-900">
                <p className="font-semibold">Recommended for you</p>
                <div className="mt-2 grid gap-2">
                  {recommendedProducts.map((product) => (
                    <div key={product.id} className="rounded-2xl bg-white p-3 shadow-sm dark:bg-slate-800">
                      <p className="font-medium">{product.name}</p>
                      <p className="text-xs text-slate-500 dark:text-slate-400">${product.price.toFixed(2)} • {product.category}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          <form onSubmit={handleSubmit} className="border-t border-black/10 p-4 dark:border-white/10">
            <div className="flex items-center gap-2">
              <button type="button" className={`inline-flex h-11 w-11 items-center justify-center rounded-2xl border ${voiceEnabled ? 'border-emerald-500 bg-emerald-500/10 text-emerald-700' : 'border-black/10 bg-white dark:border-white/10 dark:bg-white/10'} transition`} onClick={() => setVoiceEnabled((value) => !value)} aria-label="Toggle voice input">
                <Mic className="h-5 w-5" />
              </button>
              <input
                className="input flex-1"
                value={text}
                onChange={(event) => setText(event.target.value)}
                placeholder="Ask about products, orders, shipping, or cart"
                aria-label="Chat message"
              />
              <button type="submit" className="inline-flex h-11 items-center justify-center rounded-2xl bg-ink px-4 text-white transition hover:bg-black" aria-label="Send message">
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              </button>
            </div>
            <div className="mt-3 flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400">
              <button type="button" className="inline-flex items-center gap-1 text-slate-600 hover:text-ink dark:text-slate-300" onClick={clearHistory} aria-label="Clear chat history">
                <Trash2 className="h-3.5 w-3.5" /> Clear history
              </button>
              <span>{voiceEnabled ? 'Listening...' : 'Offline AI + rule-based fallback'}</span>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
