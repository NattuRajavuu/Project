import { useState } from 'react';
import toast from 'react-hot-toast';
import PageShell from '../components/PageShell';

export default function Auth() {
  const [mode, setMode] = useState('login');

  const submit = (event) => {
    event.preventDefault();
    toast.success(mode === 'login' ? 'Welcome back' : 'Account created');
  };

  return (
    <PageShell>
      <section className="section grid items-center gap-10 lg:grid-cols-[0.9fr_1fr]">
        <div>
          <p className="text-xs font-extrabold uppercase tracking-[0.25em] text-black/45 dark:text-white/45">Member space</p>
          <h1 className="mt-4 text-5xl font-extrabold tracking-tight">Your private atelier account.</h1>
          <p className="mt-5 max-w-lg leading-7 text-black/60 dark:text-white/60">
            Save wishlists, track orders, and keep your checkout details ready for the next release.
          </p>
        </div>
        <form onSubmit={submit} className="rounded-[2rem] border border-black/10 bg-white p-6 shadow-glow dark:border-white/10 dark:bg-white/10 sm:p-8">
          <div className="mb-6 grid grid-cols-2 rounded-full bg-black/5 p-1 dark:bg-white/10">
            {['login', 'register'].map((item) => (
              <button
                type="button"
                key={item}
                onClick={() => setMode(item)}
                className={`rounded-full px-4 py-3 text-sm font-bold capitalize transition ${mode === item ? 'bg-white shadow-soft dark:bg-ink' : 'text-black/50 dark:text-white/50'}`}
              >
                {item}
              </button>
            ))}
          </div>
          <div className="grid gap-4">
            {mode === 'register' && <input className="input" placeholder="Full name" required />}
            <input className="input" type="email" placeholder="Email address" required />
            <input className="input" type="password" placeholder="Password" required />
          </div>
          <button className="button-primary mt-6 w-full">{mode === 'login' ? 'Login' : 'Create account'}</button>
          <p className="mt-5 text-center text-sm text-black/50 dark:text-white/50">Demo authentication only. No backend required.</p>
        </form>
      </section>
    </PageShell>
  );
}
