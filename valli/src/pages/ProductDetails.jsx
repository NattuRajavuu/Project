import { Heart, ShoppingBag, Star } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import PageShell from '../components/PageShell';
import ProductCard from '../components/ProductCard';
import QuantityControl from '../components/QuantityControl';
import { useCart } from '../context/CartContext';
import { products } from '../data/products';
import { formatCurrency } from '../utils/formatCurrency';

export default function ProductDetails() {
  const { id } = useParams();
  const product = products.find((item) => item.id === id);
  const [quantity, setQuantity] = useState(1);
  const [image, setImage] = useState(product?.image);
  const { addToCart, toggleWishlist, wishlist } = useCart();

  useEffect(() => {
    setImage(product?.image);
    setQuantity(1);
  }, [product]);

  if (!product) {
    return (
      <PageShell>
        <section className="section text-center">
          <h1 className="text-3xl font-extrabold">Product not found</h1>
          <Link className="button-primary mt-6" to="/products">Back to shop</Link>
        </section>
      </PageShell>
    );
  }

  const active = wishlist.some((item) => item.id === product.id);
  const related = products.filter((item) => item.category === product.category && item.id !== product.id).slice(0, 3);

  return (
    <PageShell>
      <section className="section grid gap-10 lg:grid-cols-[1.05fr_0.95fr]">
        <div>
          <img src={image} alt={product.name} className="aspect-[4/3] w-full rounded-[2rem] object-cover shadow-glow" />
          <div className="mt-4 grid grid-cols-3 gap-3">
            {[product.image, ...product.gallery].map((item) => (
              <button key={item} onClick={() => setImage(item)} className="overflow-hidden rounded-2xl border border-black/10 dark:border-white/10">
                <img src={item} alt="" className="aspect-[4/3] w-full object-cover" />
              </button>
            ))}
          </div>
        </div>
        <div className="lg:pt-8">
          <p className="text-xs font-extrabold uppercase tracking-[0.25em] text-black/45 dark:text-white/45">{product.category}</p>
          <h1 className="mt-4 text-4xl font-extrabold tracking-tight sm:text-5xl">{product.name}</h1>
          <div className="mt-4 flex items-center gap-3 text-sm font-semibold text-black/55 dark:text-white/55">
            <span className="flex items-center gap-1"><Star className="h-4 w-4 fill-current" /> {product.rating}</span>
            <span>{product.tag}</span>
          </div>
          <p className="mt-6 text-3xl font-extrabold">{formatCurrency(product.price)}</p>
          <p className="mt-5 max-w-xl text-base leading-7 text-black/60 dark:text-white/60">{product.description}</p>
          <div className="mt-7">
            <p className="mb-3 text-sm font-bold">Finish</p>
            <div className="flex flex-wrap gap-2">
              {product.colors.map((color) => (
                <span key={color} className="rounded-full border border-black/10 px-4 py-2 text-sm font-semibold dark:border-white/10">{color}</span>
              ))}
            </div>
          </div>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <QuantityControl value={quantity} onChange={(next) => setQuantity(Math.max(1, next))} />
            <button className="button-primary" onClick={() => addToCart(product, quantity)}>
              <ShoppingBag className="h-4 w-4" /> Add to cart
            </button>
            <button className="button-secondary" onClick={() => toggleWishlist(product)}>
              <Heart className={`h-4 w-4 ${active ? 'fill-current' : ''}`} /> Wishlist
            </button>
          </div>
          <div className="mt-8 grid gap-3 text-sm text-black/55 dark:text-white/55">
            <p>Free returns within 30 days.</p>
            <p>Ships in recyclable premium packaging.</p>
            <p>Secure checkout with encrypted payment simulation.</p>
          </div>
        </div>
      </section>
      {related.length > 0 && (
        <section className="section py-16">
          <h2 className="mb-6 text-2xl font-extrabold">Related pieces</h2>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {related.map((item) => <ProductCard key={item.id} product={item} />)}
          </div>
        </section>
      )}
    </PageShell>
  );
}
