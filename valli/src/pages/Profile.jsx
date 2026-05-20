import { Heart, Package, Settings, User } from 'lucide-react';
import PageShell from '../components/PageShell';
import { useCart } from '../context/CartContext';
import { formatCurrency } from '../utils/formatCurrency';

export default function Profile() {
  const { wishlist, cart, totals } = useCart();

  return (
    <PageShell>
      <section className="section">
        <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <p className="text-xs font-extrabold uppercase tracking-[0.25em] text-black/45 dark:text-white/45">Dashboard</p>
            <h1 className="mt-3 text-4xl font-extrabold tracking-tight">Welcome, Atelier Member</h1>
          </div>
          <button className="button-secondary"><Settings className="h-4 w-4" /> Preferences</button>
        </div>
        <div className="grid gap-5 md:grid-cols-3">
          {[
            [Package, 'Cart value', formatCurrency(totals.total)],
            [Heart, 'Wishlist items', wishlist.length],
            [User, 'Member tier', 'Black'],
          ].map(([Icon, label, value]) => (
            <div key={label} className="rounded-[1.5rem] border border-black/10 bg-white p-6 shadow-soft dark:border-white/10 dark:bg-white/10">
              <Icon className="h-5 w-5" />
              <p className="mt-5 text-sm text-black/50 dark:text-white/50">{label}</p>
              <p className="mt-2 text-3xl font-extrabold">{value}</p>
            </div>
          ))}
        </div>
        <div className="mt-8 grid gap-5 lg:grid-cols-2">
          <div className="rounded-[1.5rem] border border-black/10 bg-white p-6 shadow-soft dark:border-white/10 dark:bg-white/10">
            <h2 className="text-xl font-extrabold">Recent orders</h2>
            <div className="mt-5 grid gap-4">
              {['LA-2048', 'LA-1982', 'LA-1844'].map((order, index) => (
                <div key={order} className="flex items-center justify-between rounded-2xl bg-black/5 p-4 text-sm dark:bg-white/10">
                  <span className="font-bold">{order}</span>
                  <span className="text-black/55 dark:text-white/55">{index === 0 ? 'Processing' : 'Delivered'}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-[1.5rem] border border-black/10 bg-white p-6 shadow-soft dark:border-white/10 dark:bg-white/10">
            <h2 className="text-xl font-extrabold">Saved cart</h2>
            <div className="mt-5 grid gap-4">
              {cart.length ? cart.map((item) => (
                <div key={item.id} className="flex items-center gap-3 rounded-2xl bg-black/5 p-3 dark:bg-white/10">
                  <img src={item.image} alt={item.name} className="h-14 w-14 rounded-xl object-cover" />
                  <div>
                    <p className="text-sm font-bold">{item.name}</p>
                    <p className="text-xs text-black/55 dark:text-white/55">Qty {item.quantity}</p>
                  </div>
                </div>
              )) : <p className="text-sm text-black/55 dark:text-white/55">No active cart items.</p>}
            </div>
          </div>
        </div>
      </section>
    </PageShell>
  );
}
