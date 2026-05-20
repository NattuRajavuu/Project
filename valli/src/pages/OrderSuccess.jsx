import { CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import PageShell from '../components/PageShell';

export default function OrderSuccess() {
  return (
    <PageShell>
      <section className="section grid min-h-[60vh] place-items-center text-center">
        <div className="max-w-lg rounded-[2rem] border border-black/10 bg-white p-10 shadow-glow dark:border-white/10 dark:bg-white/10">
          <CheckCircle2 className="mx-auto h-16 w-16" />
          <p className="mt-6 text-xs font-extrabold uppercase tracking-[0.25em] text-black/45 dark:text-white/45">Order Confirmed</p>
          <h1 className="mt-3 text-4xl font-extrabold tracking-tight">Your essentials are on their way.</h1>
          <p className="mt-4 leading-7 text-black/60 dark:text-white/60">
            A confirmation has been simulated for this demo checkout. Your order number is LA-2056.
          </p>
          <div className="mt-7 flex flex-col justify-center gap-3 sm:flex-row">
            <Link className="button-primary" to="/products">Continue shopping</Link>
            <Link className="button-secondary" to="/profile">View dashboard</Link>
          </div>
        </div>
      </section>
    </PageShell>
  );
}
