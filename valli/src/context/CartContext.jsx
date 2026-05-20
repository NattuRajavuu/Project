import { createContext, useContext, useMemo } from 'react';
import toast from 'react-hot-toast';
import { useLocalStorage } from '../hooks/useLocalStorage';

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const [cart, setCart] = useLocalStorage('luxe-cart', []);
  const [wishlist, setWishlist] = useLocalStorage('luxe-wishlist', []);
  const [theme, setTheme] = useLocalStorage('luxe-theme', 'light');

  const addToCart = (product, quantity = 1) => {
    setCart((items) => {
      const existing = items.find((item) => item.id === product.id);
      if (existing) {
        return items.map((item) => (item.id === product.id ? { ...item, quantity: item.quantity + quantity } : item));
      }
      return [...items, { ...product, quantity }];
    });
    toast.success(`${product.name} added to cart`);
  };

  const removeFromCart = (id) => setCart((items) => items.filter((item) => item.id !== id));

  const updateQuantity = (id, quantity) => {
    if (quantity < 1) return removeFromCart(id);
    setCart((items) => items.map((item) => (item.id === id ? { ...item, quantity } : item)));
  };

  const clearCart = () => setCart([]);

  const toggleWishlist = (product) => {
    setWishlist((items) => {
      const exists = items.some((item) => item.id === product.id);
      toast.success(exists ? 'Removed from wishlist' : 'Saved to wishlist');
      return exists ? items.filter((item) => item.id !== product.id) : [...items, product];
    });
  };

  const totals = useMemo(() => {
    const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const shipping = subtotal > 0 ? 18 : 0;
    return { subtotal, shipping, total: subtotal + shipping };
  }, [cart]);

  const value = {
    cart,
    wishlist,
    theme,
    setTheme,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    toggleWishlist,
    totals,
    cartCount: cart.reduce((sum, item) => sum + item.quantity, 0),
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export const useCart = () => useContext(CartContext);
