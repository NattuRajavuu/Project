import { CreditCard, Lock } from 'lucide-react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import PageShell from '../components/PageShell';
import { useCart } from '../context/CartContext';
import { formatCurrency } from '../utils/formatCurrency';

export default function Checkout() {
  const { cart, totals, clearCart } = useCart();
  const navigate = useNavigate();

  const submit = (event) => {
    event.preventDefault();
    clearCart();
    toast.success('Order placed');
    navigate('/success');
  };

  return (
    <PageShell>
      <section className="section grid gap-8 lg:grid-cols-[1fr_380px]">
        <form onSubmit={submit} className="rounded-[2rem] border border-black/10 bg-white p-6 shadow-soft dark:border-white/10 dark:bg-white/10 sm:p-8">
          <p className="text-xs font-extrabold uppercase tracking-[0.25em] text-black/45 dark:text-white/45">Secure Checkout</p>
          <h1 className="mt-3 text-4xl font-extrabold tracking-tight">Complete your order</h1>
          <div className="mt-8 grid gap-5">
            <div className="grid gap-4 sm:grid-cols-2">
              <input className="input" placeholder="First name" required />
              <input className="input" placeholder="Last name" required />
            </div>
            <input className="input" type="email" placeholder="Email address" required />
            <input className="input" placeholder="Street address" required />
            <div className="grid gap-4 sm:grid-cols-3">
              <input className="input" placeholder="City" required />
              <input className="input" placeholder="State" required />
              <input className="input" placeholder="ZIP" required />
            </div>
            <div className="mt-3 rounded-[1.5rem] border border-black/10 p-5 dark:border-white/10">
              <div className="mb-4 flex items-center gap-2 font-bold"><CreditCard className="h-5 w-5" /> Payment</div>
              <div className="grid gap-4">
                <input className="input" placeholder="Card number" required />
                <div className="grid gap-4 sm:grid-cols-2">
                  <input className="input" placeholder="MM / YY" required />
                  <input className="input" placeholder="CVC" required />
                </div>
              </div>
            </div>
          </div>
          <button className="button-primary mt-8 w-full" disabled={!cart.length}>
            <Lock className="h-4 w-4" /> Place order
          </button>
        </form>
        <aside className="h-fit rounded-[2rem] border border-black/10 bg-white p-6 shadow-soft dark:border-white/10 dark:bg-white/10">
          <h2 className="text-xl font-extrabold">Summary</h2>
          <div className="mt-5 grid gap-4">
            {cart.length ? cart.map((item) => (
              <div key={item.id} className="flex gap-3">
                <img src={item.image} alt={item.name} className="h-16 w-16 rounded-2xl object-cover" />
                <div className="flex-1">
                  <p className="text-sm font-bold">{item.name}</p>
                  <p className="text-xs text-black/50 dark:text-white/50">Qty {item.quantity}</p>
                </div>
                <strong className="text-sm">{formatCurrency(item.price * item.quantity)}</strong>
              </div>
            )) : <p className="text-sm text-black/55 dark:text-white/55">Your cart is empty.</p>}
          </div>
          <div className="mt-6 grid gap-3 border-t border-black/10 pt-5 text-sm dark:border-white/10">
            <div className="flex justify-between"><span>Subtotal</span><strong>{formatCurrency(totals.subtotal)}</strong></div>
            <div className="flex justify-between"><span>Shipping</span><strong>{formatCurrency(totals.shipping)}</strong></div>
            <div className="flex justify-between text-lg"><span>Total</span><strong>{formatCurrency(totals.total)}</strong></div>
          </div>
        </aside>
      </section>
    </PageShell>
  );
}
