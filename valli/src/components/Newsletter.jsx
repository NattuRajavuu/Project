import { Send } from 'lucide-react';
import toast from 'react-hot-toast';

export default function Newsletter() {
  const submit = (event) => {
    event.preventDefault();
    toast.success('You are on the list');
    event.currentTarget.reset();
  };

  return (
    <section className="section py-16">
      <div className="grid gap-8 rounded-[2rem] bg-ink p-8 text-white shadow-glow dark:bg-white dark:text-ink md:grid-cols-[1fr_0.9fr] md:p-12">
        <div>
          <p className="text-xs font-extrabold uppercase tracking-[0.25em] opacity-60">Private Notes</p>
          <h2 className="mt-3 text-3xl font-extrabold tracking-tight">New drops, quiet edits, early access.</h2>
        </div>
        <form onSubmit={submit} className="flex flex-col gap-3 sm:flex-row md:self-end">
          <input className="min-h-12 flex-1 rounded-full border border-white/20 bg-white/10 px-5 text-sm outline-none placeholder:text-white/50 dark:border-black/10 dark:bg-black/5 dark:placeholder:text-black/40" placeholder="Email address" type="email" required />
          <button className="inline-flex min-h-12 items-center justify-center gap-2 rounded-full bg-white px-5 text-sm font-bold text-ink dark:bg-ink dark:text-white">
            <Send className="h-4 w-4" /> Join
          </button>
        </form>
      </div>
    </section>
  );
}
