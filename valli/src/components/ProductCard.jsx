import { Heart, ShoppingBag, Star } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { fadeUp } from '../animations/variants';
import { useCart } from '../context/CartContext';
import { formatCurrency } from '../utils/formatCurrency';

export default function ProductCard({ product }) {
  const { addToCart, toggleWishlist, wishlist } = useCart();
  const active = wishlist.some((item) => item.id === product.id);

  return (
    <motion.article variants={fadeUp} className="group overflow-hidden rounded-[2rem] border border-black/10 bg-white shadow-soft transition hover:-translate-y-1 hover:shadow-glow dark:border-white/10 dark:bg-white/10">
      <Link to={`/products/${product.id}`} className="block overflow-hidden bg-mist/50">
        <img src={product.image} alt={product.name} className="aspect-[4/3] w-full object-cover transition duration-700 group-hover:scale-105" loading="lazy" />
      </Link>
      <div className="p-5">
        <div className="mb-3 flex items-center justify-between gap-3">
          <span className="rounded-full bg-black/5 px-3 py-1 text-xs font-bold text-black/55 dark:bg-white/10 dark:text-white/60">{product.tag}</span>
          <span className="flex items-center gap-1 text-xs font-semibold text-black/55 dark:text-white/55">
            <Star className="h-3.5 w-3.5 fill-current" /> {product.rating}
          </span>
        </div>
        <Link to={`/products/${product.id}`} className="text-lg font-bold tracking-tight hover:underline">
          {product.name}
        </Link>
        <p className="mt-2 line-clamp-2 min-h-10 text-sm leading-5 text-black/55 dark:text-white/55">{product.description}</p>
        <div className="mt-5 flex items-center justify-between gap-3">
          <span className="text-lg font-extrabold">{formatCurrency(product.price)}</span>
          <div className="flex gap-2">
            <button className="button-secondary !h-11 !w-11 !rounded-full !p-0" onClick={() => toggleWishlist(product)} aria-label="Toggle wishlist">
              <Heart className={`h-4 w-4 ${active ? 'fill-current' : ''}`} />
            </button>
            <button className="button-primary !h-11 !w-11 !rounded-full !p-0" onClick={() => addToCart(product)} aria-label="Add to cart">
              <ShoppingBag className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </motion.article>
  );
}
