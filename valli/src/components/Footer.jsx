import { Instagram, Linkedin, Twitter } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="border-t border-black/5 bg-white/45 py-12 dark:border-white/10 dark:bg-white/5">
      <div className="section grid gap-8 md:grid-cols-[1.5fr_1fr_1fr]">
        <div>
          <h2 className="text-xl font-extrabold">Luxe Atelier</h2>
          <p className="mt-3 max-w-md text-sm leading-6 text-black/55 dark:text-white/55">
            Curated objects for quieter work, richer travel, and better everyday rituals.
          </p>
          <div className="mt-5 flex gap-2">
            {[Instagram, Twitter, Linkedin].map((Icon, index) => (
              <a key={index} href="#" className="button-secondary !h-10 !w-10 !rounded-full !p-0" aria-label="Social link">
                <Icon className="h-4 w-4" />
              </a>
            ))}
          </div>
        </div>
        <div>
          <h3 className="text-sm font-bold">Explore</h3>
          <div className="mt-4 grid gap-3 text-sm text-black/55 dark:text-white/55">
            <Link to="/products">Products</Link>
            <Link to="/wishlist">Wishlist</Link>
            <Link to="/cart">Cart</Link>
          </div>
        </div>
        <div>
          <h3 className="text-sm font-bold">Member Care</h3>
          <div className="mt-4 grid gap-3 text-sm text-black/55 dark:text-white/55">
            <Link to="/profile">Profile</Link>
            <Link to="/auth">Login</Link>
            <a href="mailto:care@luxeatelier.test">care@luxeatelier.test</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
