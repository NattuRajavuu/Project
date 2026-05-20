import { Moon, Sun } from 'lucide-react';
import { useCart } from '../context/CartContext';

export default function ThemeToggle() {
  const { theme, setTheme } = useCart();
  const dark = theme === 'dark';

  return (
    <button className="button-secondary !h-11 !w-11 !rounded-full !p-0" onClick={() => setTheme(dark ? 'light' : 'dark')} aria-label="Toggle dark mode">
      {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
    </button>
  );
}
