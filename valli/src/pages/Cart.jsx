import { ShoppingBag, Trash2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import PageShell from '../components/PageShell';
import QuantityControl from '../components/QuantityControl';
import { useCart } from '../context/CartContext';
import { formatCurrency } from '../utils/formatCurrency';

export default function Cart() {
  const { cart, totals, updateQuantity, removeFromCart } = useCart();

  if (!cart.length) {
    return (
      <PageShell>
        <section className="section grid min-h-[55vh] place-items-center text-center">
          <div className="max-w-md">
            <div className="mx-auto grid h-20 w-20 place-items-center rounded-full bg-white shadow-soft dark:bg-white/10">
              <ShoppingBag className="h-8 w-8" />
            </div>
            <h1 className="mt-6 text-3xl font-extrabold">Your cart is beautifully empty</h1>
            <p className="mt-3 text-black/55 dark:text-white/55">Add a few refined essentials and they will appear here.</p>
            <Link className="button-primary mt-7" to="/products">Start shopping</Link>
          </div>
        </section>
      </PageShell>
    );
  }

  return (
    <PageShell>
      <section className="section grid gap-8 lg:grid-cols-[1fr_380px]">
        <div>
          <h1 className="mb-6 text-4xl font-extrabold tracking-tight">Shopping cart</h1>
          <div className="grid gap-4">
            {cart.map((item) => (
              <article key={item.id} className="grid gap-4 rounded-[1.5rem] border border-black/10 bg-white p-4 shadow-soft dark:border-white/10 dark:bg-white/10 sm:grid-cols-[120px_1fr_auto]">
                <img src={item.image} alt={item.name} className="aspect-square w-full rounded-2xl object-cover sm:w-[120px]" />
                <div>
                  <h2 className="font-bold">{item.name}</h2>
                  <p className="mt-1 text-sm text-black/55 dark:text-white/55">{item.category}</p>
                  <p className="mt-3 text-lg font-extrabold">{formatCurrency(item.price)}</p>
                </div>
                <div className="flex items-center justify-between gap-3 sm:flex-col sm:items-end">
                  <button className="button-secondary !h-10 !w-10 !rounded-full !p-0" onClick={() => removeFromCart(item.id)} aria-label="Remove item">
                    <Trash2 className="h-4 w-4" />
                  </button>
                  <QuantityControl value={item.quantity} onChange={(next) => updateQuantity(item.id, next)} />
                </div>
              </article>
            ))}
          </div>
        </div>
        <aside className="h-fit rounded-[2rem] border border-black/10 bg-white p-6 shadow-soft dark:border-white/10 dark:bg-white/10">
          <h2 className="text-xl font-extrabold">Order summary</h2>
          <div className="mt-6 grid gap-3 text-sm">
            <div className="flex justify-between"><span>Subtotal</span><strong>{formatCurrency(totals.subtotal)}</strong></div>
            <div className="flex justify-between"><span>Shipping</span><strong>{formatCurrency(totals.shipping)}</strong></div>
            <div className="border-t border-black/10 pt-4 text-lg dark:border-white/10 flex justify-between"><span>Total</span><strong>{formatCurrency(totals.total)}</strong></div>
          </div>
          <Link className="button-primary mt-6 w-full" to="/checkout">Checkout</Link>
        </aside>
      </section>
    </PageShell>
  );
}
