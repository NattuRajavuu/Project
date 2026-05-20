import { Menu, Search, ShoppingBag, User, X } from 'lucide-react';
import { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import ThemeToggle from './ThemeToggle';

const links = [
  { to: '/', label: 'Home' },
  { to: '/products', label: 'Shop' },
  { to: '/wishlist', label: 'Wishlist' },
  { to: '/profile', label: 'Profile' },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const { cartCount } = useCart();
  const navigate = useNavigate();

  const submit = (event) => {
    event.preventDefault();
    navigate(`/products${query ? `?search=${encodeURIComponent(query)}` : ''}`);
    setOpen(false);
  };

  return (
    <header className="sticky top-0 z-50 border-b border-black/5 bg-pearl/75 backdrop-blur-2xl dark:border-white/10 dark:bg-ink/75">
      <nav className="section flex h-20 items-center justify-between gap-4">
        <Link to="/" className="text-lg font-extrabold tracking-tight" aria-label="Luxe Atelier home">
          Luxe Atelier
        </Link>
        <div className="hidden items-center gap-7 lg:flex">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `text-sm font-medium transition hover:text-black dark:hover:text-white ${isActive ? 'text-black dark:text-white' : 'text-black/55 dark:text-white/55'}`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </div>
        <div className="hidden flex-1 justify-end lg:flex">
          <form onSubmit={submit} className="relative w-full max-w-xs">
            <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-black/40 dark:text-white/40" />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className="input py-2.5 pl-10"
              placeholder="Search essentials"
              aria-label="Search products"
            />
          </form>
        </div>
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Link to="/auth" className="button-secondary hidden !h-11 !w-11 !rounded-full !p-0 sm:inline-flex" aria-label="Login or register">
            <User className="h-4 w-4" />
          </Link>
          <Link to="/cart" className="button-secondary relative !h-11 !w-11 !rounded-full !p-0" aria-label="Cart">
            <ShoppingBag className="h-4 w-4" />
            {cartCount > 0 && (
              <span className="absolute -right-1 -top-1 grid h-5 min-w-5 place-items-center rounded-full bg-ink px-1 text-[11px] font-bold text-white dark:bg-white dark:text-ink">
                {cartCount}
              </span>
            )}
          </Link>
          <button className="button-secondary !h-11 !w-11 !rounded-full !p-0 lg:hidden" onClick={() => setOpen((value) => !value)} aria-label="Toggle menu">
            {open ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </button>
        </div>
      </nav>
      {open && (
        <div className="section pb-5 lg:hidden">
          <form onSubmit={submit} className="relative mb-4">
            <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-black/40 dark:text-white/40" />
            <input value={query} onChange={(event) => setQuery(event.target.value)} className="input pl-10" placeholder="Search essentials" />
          </form>
          <div className="grid gap-2 rounded-3xl border border-black/10 bg-white/80 p-3 dark:border-white/10 dark:bg-white/10">
            {links.map((link) => (
              <NavLink key={link.to} to={link.to} onClick={() => setOpen(false)} className="rounded-2xl px-4 py-3 text-sm font-semibold hover:bg-black/5 dark:hover:bg-white/10">
                {link.label}
              </NavLink>
            ))}
            <NavLink to="/auth" onClick={() => setOpen(false)} className="rounded-2xl px-4 py-3 text-sm font-semibold hover:bg-black/5 dark:hover:bg-white/10">
              Login
            </NavLink>
          </div>
        </div>
      )}
    </header>
  );
}
