import { useEffect, useState } from 'react';

const ADMIN_TOKEN = 'dev-token';

const fetchJson = async (url, options = {}) => {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-Admin-Token': ADMIN_TOKEN,
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
};

export default function Admin() {
  const [faqs, setFaqs] = useState([]);
  const [intents, setIntents] = useState([]);
  const [faqForm, setFaqForm] = useState({ topic: '', question: '', answer: '', keywords: '' });
  const [intentForm, setIntentForm] = useState({ intent: '', trigger_keywords: '', response: '' });
  const [error, setError] = useState(null);

  const loadData = async () => {
    try {
      const [faqData, intentData] = await Promise.all([fetchJson('/api/admin/faqs'), fetchJson('/api/admin/intents')]);
      setFaqs(faqData);
      setIntents(intentData);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleFaqSubmit = async (event) => {
    event.preventDefault();
    try {
      await fetchJson('/api/admin/faqs', {
        method: 'POST',
        body: JSON.stringify(faqForm),
      });
      setFaqForm({ topic: '', question: '', answer: '', keywords: '' });
      loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleIntentSubmit = async (event) => {
    event.preventDefault();
    try {
      await fetchJson('/api/admin/intents', {
        method: 'POST',
        body: JSON.stringify(intentForm),
      });
      setIntentForm({ intent: '', trigger_keywords: '', response: '' });
      loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  const removeFaq = async (id) => {
    try {
      await fetchJson('/api/admin/faqs', {
        method: 'DELETE',
        body: JSON.stringify({ id }),
      });
      loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  const removeIntent = async (id) => {
    try {
      await fetchJson('/api/admin/intents', {
        method: 'DELETE',
        body: JSON.stringify({ id }),
      });
      loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <section className="section py-16">
      <div className="mx-auto max-w-5xl rounded-[32px] border border-black/10 bg-white/90 p-8 shadow-soft dark:border-white/10 dark:bg-slate-900/90">
        <h1 className="text-3xl font-bold">Offline Chatbot Admin</h1>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Manage FAQ responses and keyword intents locally.</p>
        {error && <div className="mt-4 rounded-3xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-500/20 dark:bg-red-500/10">{error}</div>}
        <div className="mt-8 grid gap-8 lg:grid-cols-2">
          <div className="rounded-3xl border border-black/10 bg-slate-50 p-6 dark:border-white/10 dark:bg-slate-900">
            <h2 className="text-xl font-semibold">Add FAQ</h2>
            <form onSubmit={handleFaqSubmit} className="mt-4 space-y-4">
              {['topic', 'question', 'answer', 'keywords'].map((field) => (
                <label key={field} className="block text-sm font-medium text-slate-700 dark:text-slate-200">
                  {field.charAt(0).toUpperCase() + field.slice(1)}
                  <input
                    value={faqForm[field]}
                    onChange={(event) => setFaqForm((prev) => ({ ...prev, [field]: event.target.value }))}
                    className="input mt-2 w-full"
                    required
                  />
                </label>
              ))}
              <button type="submit" className="button-primary">Save FAQ</button>
            </form>
          </div>
          <div className="rounded-3xl border border-black/10 bg-slate-50 p-6 dark:border-white/10 dark:bg-slate-900">
            <h2 className="text-xl font-semibold">Add Intent</h2>
            <form onSubmit={handleIntentSubmit} className="mt-4 space-y-4">
              {['intent', 'trigger_keywords', 'response'].map((field) => (
                <label key={field} className="block text-sm font-medium text-slate-700 dark:text-slate-200">
                  {field === 'trigger_keywords' ? 'Trigger Keywords' : field.charAt(0).toUpperCase() + field.slice(1)}
                  <input
                    value={intentForm[field]}
                    onChange={(event) => setIntentForm((prev) => ({ ...prev, [field]: event.target.value }))}
                    className="input mt-2 w-full"
                    required
                  />
                </label>
              ))}
              <button type="submit" className="button-primary">Save Intent</button>
            </form>
          </div>
        </div>
        <div className="mt-10 space-y-6">
          <div className="rounded-3xl border border-black/10 bg-slate-50 p-6 dark:border-white/10 dark:bg-slate-900">
            <h2 className="text-xl font-semibold">FAQ Library</h2>
            <div className="mt-4 space-y-3">
              {faqs.map((faq) => (
                <div key={faq.id} className="rounded-3xl border border-black/10 bg-white p-4 dark:border-white/10 dark:bg-slate-800">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="text-sm font-semibold">{faq.topic}</p>
                      <p className="mt-1 text-sm text-slate-500 dark:text-slate-300">{faq.question}</p>
                    </div>
                    <button onClick={() => removeFaq(faq.id)} className="text-sm text-red-600 hover:text-red-700 dark:text-red-400">Delete</button>
                  </div>
                  <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">{faq.answer}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-3xl border border-black/10 bg-slate-50 p-6 dark:border-white/10 dark:bg-slate-900">
            <h2 className="text-xl font-semibold">Intent Library</h2>
            <div className="mt-4 space-y-3">
              {intents.map((item) => (
                <div key={item.id} className="rounded-3xl border border-black/10 bg-white p-4 dark:border-white/10 dark:bg-slate-800">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="text-sm font-semibold">{item.intent}</p>
                      <p className="mt-1 text-sm text-slate-500 dark:text-slate-300">Triggers: {item.trigger_keywords}</p>
                    </div>
                    <button onClick={() => removeIntent(item.id)} className="text-sm text-red-600 hover:text-red-700 dark:text-red-400">Delete</button>
                  </div>
                  <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">{item.response}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
