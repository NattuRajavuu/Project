import { Heart } from 'lucide-react';
import { Link } from 'react-router-dom';
import PageShell from '../components/PageShell';
import ProductCard from '../components/ProductCard';
import { useCart } from '../context/CartContext';

export default function Wishlist() {
  const { wishlist } = useCart();

  return (
    <PageShell>
      <section className="section">
        <div className="mb-8">
          <p className="text-xs font-extrabold uppercase tracking-[0.25em] text-black/45 dark:text-white/45">Saved</p>
          <h1 className="mt-3 text-4xl font-extrabold tracking-tight">Wishlist</h1>
        </div>
        {wishlist.length ? (
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {wishlist.map((product) => <ProductCard key={product.id} product={product} />)}
          </div>
        ) : (
          <div className="grid min-h-[45vh] place-items-center rounded-[2rem] border border-black/10 bg-white p-10 text-center shadow-soft dark:border-white/10 dark:bg-white/10">
            <div>
              <Heart className="mx-auto h-10 w-10" />
              <h2 className="mt-5 text-2xl font-extrabold">No saved pieces yet</h2>
              <p className="mt-2 text-black/55 dark:text-white/55">Tap the heart on any product to keep it close.</p>
              <Link className="button-primary mt-6" to="/products">Browse products</Link>
            </div>
          </div>
        )}
      </section>
    </PageShell>
  );
}
