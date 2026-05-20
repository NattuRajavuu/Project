const products = [
  {
    id: 'aura-max',
    name: 'Aura Max Headphones',
    category: 'Audio',
    price: 549,
    rating: 4.9,
    tag: 'Signature',
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'Studio-grade wireless headphones with spatial audio, soft memory foam, and an all-day battery.',
    colors: ['Graphite', 'Pearl', 'Silver'],
    features: ['Adaptive noise cancellation', 'Personalized spatial audio', '40-hour battery life'],
    specs: { Material: 'Anodized aluminum, memory foam', Battery: '40 hours', Connectivity: 'Bluetooth 5.3', Warranty: '2 years' },
  },
  {
    id: 'nova-watch',
    name: 'Nova Ceramic Watch',
    category: 'Wearables',
    price: 799,
    rating: 4.8,
    tag: 'New',
    image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'A polished ceramic smartwatch with health intelligence, crisp display, and refined bands.',
    colors: ['Porcelain', 'Obsidian', 'Mist'],
    features: ['Health and sleep insights', 'Sapphire glass display', 'Water resistant ceramic case'],
    specs: { Case: 'Ceramic 44mm', Display: 'Always-on OLED', Battery: '36 hours', Sensors: 'Heart, oxygen, temperature' },
  },
  {
    id: 'halo-lamp',
    name: 'Halo Ambient Lamp',
    category: 'Home',
    price: 320,
    rating: 4.7,
    tag: 'Home Edit',
    image: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'A sculptural lamp with warm dimming, touch controls, and soft indirect glow.',
    colors: ['Sandstone', 'Charcoal', 'White'],
    features: ['Soft warm dimming', 'Touch-sensitive base', 'Energy-efficient LED core'],
    specs: { Height: '18 in', Brightness: '900 lumens', Temperature: '2200K-3000K', Power: 'USB-C adapter' },
  },
  {
    id: 'monolith-speaker',
    name: 'Monolith Speaker',
    category: 'Audio',
    price: 680,
    rating: 4.9,
    tag: 'Best Seller',
    image: 'https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1589003077984-894e133dabab?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'Room-filling sound in a minimal aluminum body with adaptive room tuning.',
    colors: ['Black', 'Aluminum'],
    features: ['Adaptive room tuning', 'Deep balanced bass', 'Multi-room wireless pairing'],
    specs: { Drivers: 'Dual woofer, dual tweeter', Power: '120W', Connectivity: 'Wi-Fi, Bluetooth, AirPlay', Weight: '6.8 lb' },
  },
  {
    id: 'arc-sunglasses',
    name: 'Arc Titanium Sunglasses',
    category: 'Travel',
    price: 260,
    rating: 4.6,
    tag: 'Limited',
    image: 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1509695507497-903c140c43b0?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'Featherweight titanium frames with polarized lenses and a quiet luxury silhouette.',
    colors: ['Smoke', 'Champagne', 'Black'],
    features: ['Polarized UV400 lenses', 'Featherweight titanium frame', 'Hand-finished hinges'],
    specs: { Frame: 'Titanium', Lenses: 'Polarized UV400', Weight: '24 g', Included: 'Leather case, cloth' },
  },
  {
    id: 'slab-dock',
    name: 'Slab Charging Dock',
    category: 'Desk',
    price: 180,
    rating: 4.8,
    tag: 'Essential',
    image: 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'A machined multi-device dock that keeps your workspace calm, charged, and cable-light.',
    colors: ['Silver', 'Graphite'],
    features: ['Three-device charging', 'Weighted machined body', 'Cable-concealing channel'],
    specs: { Output: '15W wireless, 30W USB-C', Material: 'Aluminum', Cable: 'Braided USB-C', Footprint: '8.2 x 3.1 in' },
  },
  {
    id: 'linen-tote',
    name: 'Linen Weekender Tote',
    category: 'Travel',
    price: 340,
    rating: 4.7,
    tag: 'Travel Edit',
    image: 'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1594223274512-ad4803739b7c?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'A structured travel tote with coated linen canvas, leather trim, and a padded device sleeve.',
    colors: ['Natural', 'Carbon', 'Olive'],
    features: ['Padded laptop sleeve', 'Water-resistant lining', 'Pass-through luggage strap'],
    specs: { Volume: '32 L', Material: 'Coated linen canvas', Sleeve: 'Up to 16 in laptop', Hardware: 'Brushed nickel' },
  },
  {
    id: 'marble-tray',
    name: 'Marble Ritual Tray',
    category: 'Home',
    price: 210,
    rating: 4.8,
    tag: 'Stone Series',
    image: 'https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1602872030219-ad2b9a54315c?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'A honed marble tray for fragrance, keys, watches, and the small objects that deserve a place.',
    colors: ['Calacatta', 'Nero', 'Travertine'],
    features: ['Hand-finished stone', 'Felt-protected base', 'Naturally unique veining'],
    specs: { Material: 'Natural marble', Size: '12 x 8 in', Finish: 'Honed matte', Origin: 'Italy' },
  },
  {
    id: 'folio-keyboard',
    name: 'Folio Keyboard Case',
    category: 'Desk',
    price: 240,
    rating: 4.6,
    tag: 'Work Kit',
    image: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'A slim keyboard folio with quiet keys, adjustable viewing angles, and premium vegan leather.',
    colors: ['Black', 'Stone', 'Moss'],
    features: ['Backlit quiet keys', 'Magnetic floating stand', 'Large glass trackpad'],
    specs: { Compatibility: '11-13 in tablets', Battery: '90 days', Charging: 'USB-C', Material: 'Vegan leather' },
  },
  {
    id: 'pure-bottle',
    name: 'Pure Steel Bottle',
    category: 'Travel',
    price: 95,
    rating: 4.8,
    tag: 'Daily Carry',
    image: 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1523362628745-0c100150b504?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1610824352934-c10d87b700cc?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'A vacuum-insulated bottle with a ceramic-lined interior and a seamless satin finish.',
    colors: ['Steel', 'Ink', 'Bone'],
    features: ['Ceramic-lined interior', '24-hour cold retention', 'Leakproof magnetic cap'],
    specs: { Capacity: '750 ml', Material: '18/8 stainless steel', Insulation: 'Double-wall vacuum', Weight: '430 g' },
  },
  {
    id: 'orb-diffuser',
    name: 'Orb Aroma Diffuser',
    category: 'Home',
    price: 175,
    rating: 4.7,
    tag: 'Wellness',
    image: 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'A quiet ceramic diffuser with soft mist, warm ambient light, and automatic shutoff.',
    colors: ['Clay', 'White', 'Graphite'],
    features: ['Ultrasonic quiet mist', 'Warm ambient light', 'Automatic shutoff'],
    specs: { Capacity: '180 ml', Runtime: '8 hours', Material: 'Glazed ceramic', Coverage: '350 sq ft' },
  },
  {
    id: 'studio-pen',
    name: 'Studio Rollerball Pen',
    category: 'Desk',
    price: 125,
    rating: 4.9,
    tag: 'Writing',
    image: 'https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?auto=format&fit=crop&w=1200&q=85',
    gallery: [
      'https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=85',
      'https://images.unsplash.com/photo-1518655048521-f130df041f66?auto=format&fit=crop&w=1200&q=85',
    ],
    description: 'A balanced rollerball pen machined from brass with a satin lacquer finish and smooth refill.',
    colors: ['Black Lacquer', 'Brass', 'Silver'],
    features: ['Balanced brass body', 'Smooth archival refill', 'Magnetic cap closure'],
    specs: { Material: 'Brass', Refill: '0.7 mm rollerball', Length: '5.4 in', Weight: '42 g' },
  },
];

const categories = ['All', ...new Set(products.map((product) => product.category))];

const app = document.querySelector('#app');
const toastEl = document.querySelector('#toast');
const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
let cart = read('luxe-python-cart', []);
let wishlist = read('luxe-python-wishlist', []);
let theme = read('luxe-python-theme', 'light');

function read(key, fallback) {
  try {
    return JSON.parse(localStorage.getItem(key)) ?? fallback;
  } catch {
    return fallback;
  }
}

function write(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function toast(message) {
  toastEl.textContent = message;
  toastEl.classList.add('show');
  setTimeout(() => toastEl.classList.remove('show'), 1800);
}

function updateTheme() {
  document.documentElement.classList.toggle('dark', theme === 'dark');
  write('luxe-python-theme', theme);
}

function totals() {
  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const shipping = subtotal ? 18 : 0;
  return { subtotal, shipping, total: subtotal + shipping };
}

function updateCartCount() {
  document.querySelector('#cartCount').textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
}

function addToCart(id, quantity = 1) {
  const product = products.find((item) => item.id === id);
  const existing = cart.find((item) => item.id === id);
  if (existing) existing.quantity += quantity;
  else cart.push({ ...product, quantity });
  write('luxe-python-cart', cart);
  updateCartCount();
  toast(`${product.name} added to cart`);
}

function setQuantity(id, quantity) {
  if (quantity < 1) cart = cart.filter((item) => item.id !== id);
  else cart = cart.map((item) => (item.id === id ? { ...item, quantity } : item));
  write('luxe-python-cart', cart);
  updateCartCount();
  render();
}

function toggleWishlist(id) {
  const product = products.find((item) => item.id === id);
  const exists = wishlist.some((item) => item.id === id);
  wishlist = exists ? wishlist.filter((item) => item.id !== id) : [...wishlist, product];
  write('luxe-python-wishlist', wishlist);
  toast(exists ? 'Removed from wishlist' : 'Saved to wishlist');
  render();
}

function productCard(product) {
  const saved = wishlist.some((item) => item.id === product.id);
  return `
    <article class="product-card">
      <a href="#product/${product.id}"><img src="${product.image}" alt="${product.name}" loading="lazy"></a>
      <div class="product-info">
        <div class="row" style="justify-content:space-between">
          <span class="tag">${product.tag}</span>
          <span class="muted">Star ${product.rating}</span>
        </div>
        <h3 style="margin:16px 0 8px"><a href="#product/${product.id}">${product.name}</a></h3>
        <p class="muted">${product.description}</p>
        <div class="row" style="justify-content:space-between;margin-top:18px">
          <span class="price">${money.format(product.price)}</span>
          <div class="row">
            <button class="icon-button" onclick="toggleWishlist('${product.id}')" aria-label="Wishlist">${saved ? '♥' : '♡'}</button>
            <button class="icon-button" onclick="addToCart('${product.id}')" aria-label="Add to cart">Bag</button>
          </div>
        </div>
        <div class="product-actions">
          <a class="button-secondary" href="#product/${product.id}">View specs</a>
          <a class="button-primary" href="#payment/${product.id}">Buy now</a>
        </div>
      </div>
    </article>
  `;
}

function home() {
  return `
    <div class="page">
      <section class="section hero">
        <div>
          <p class="eyebrow">Minimal luxury objects</p>
          <h1>Designed essentials for a calmer everyday.</h1>
          <p class="lead">Premium technology, refined home pieces, and travel accessories curated with quiet confidence.</p>
          <div class="hero-actions">
            <a class="button-primary" href="#products">Shop collection</a>
            <a class="button-secondary" href="#wishlist">View wishlist</a>
          </div>
        </div>
        <div class="hero-media">
          <img src="https://images.unsplash.com/photo-1491933382434-500287f9b54b?auto=format&fit=crop&w=1400&q=85" alt="Premium desk setup">
          <div class="glass-badge">
            <div><span class="eyebrow">Featured</span><strong style="display:block;margin-top:5px">Monolith Speaker</strong></div>
            <strong>${money.format(680)}</strong>
          </div>
        </div>
      </section>
      <section class="section grid-4">
        ${['Express Delivery|Fast, tracked shipping worldwide.', 'Secure Checkout|Protected payments and privacy.', 'Premium Curation|Only objects worth owning.', 'Member Access|Early drops and private edits.'].map((item) => {
          const [title, text] = item.split('|');
          return `<div class="card"><h3>${title}</h3><p class="muted">${text}</p></div>`;
        }).join('')}
      </section>
      <section class="section">
        <div class="section-heading"><p class="eyebrow">Shop by mood</p><h2>Category edits</h2><p class="muted">Focused collections for sound, work, home, and motion.</p></div>
        <div class="grid-3">
          ${['Audio', 'Wearables', 'Home'].map((cat) => {
            const product = products.find((item) => item.category === cat);
            return `<a class="category-card" href="#products?category=${cat}"><img src="${product.image}" alt="${cat}"><div><h2>${cat}</h2><p>Explore edit</p></div></a>`;
          }).join('')}
        </div>
      </section>
      <section class="section">
        <div class="section-heading"><p class="eyebrow">Featured</p><h2>Objects with presence</h2><p class="muted">Premium pieces chosen for performance, silhouette, and daily usefulness.</p></div>
        <div class="product-grid">${products.slice(0, 3).map(productCard).join('')}</div>
      </section>
      <section class="section">
        <div class="section-heading"><p class="eyebrow">Notes</p><h2>Loved by detail people</h2></div>
        <div class="grid-3">
          ${['The experience feels calmer than any online store I use. Checkout was effortless.', 'Beautiful curation, fast interactions, and the details feel genuinely premium.', 'I came for headphones and left with a wishlist full of objects I actually want.'].map((text) => `<blockquote class="card"><p>"${text}"</p></blockquote>`).join('')}
        </div>
      </section>
      <section class="section">
        <div class="newsletter">
          <div><p class="eyebrow">Private Notes</p><h2>New drops, quiet edits, early access.</h2></div>
          <form onsubmit="event.preventDefault(); this.reset(); toast('You are on the list')">
            <input placeholder="Email address" type="email" required>
            <button class="button-secondary">Join</button>
          </form>
        </div>
      </section>
    </div>
  `;
}

function productsPage() {
  const query = new URLSearchParams(location.hash.split('?')[1] || '');
  const selectedCategory = query.get('category') || 'All';
  const search = query.get('search') || '';
  let list = products.filter((item) => selectedCategory === 'All' || item.category === selectedCategory);
  list = list.filter((item) => `${item.name} ${item.description}`.toLowerCase().includes(search.toLowerCase()));
  return `
    <section class="section page">
      <div class="section-heading"><p class="eyebrow">The Collection</p><h1>Shop refined essentials</h1><p class="muted">Filter by category, search by need, and sort the collection your way.</p></div>
      <div class="filters">
        <input class="input" id="pageSearch" placeholder="Search products" value="${search}">
        <select id="categoryFilter">${categories.map((cat) => `<option ${cat === selectedCategory ? 'selected' : ''}>${cat}</option>`).join('')}</select>
        <select id="sortFilter"><option value="featured">Featured</option><option value="low">Price: Low to High</option><option value="high">Price: High to Low</option><option value="rating">Top Rated</option></select>
      </div>
      <p class="muted"><strong>${list.length}</strong> products</p>
      <div class="product-grid" id="productGrid">${list.map(productCard).join('') || '<div class="panel empty"><div><h2>No products found</h2><p class="muted">Try another category or search term.</p></div></div>'}</div>
    </section>
  `;
}

function productDetails(id) {
  const product = products.find((item) => item.id === id);
  if (!product) return notFound();
  const related = products.filter((item) => item.category === product.category && item.id !== product.id).slice(0, 3);
  return `
    <div class="page">
      <section class="section details">
        <div>
          <img class="product-main-image" id="mainProductImage" src="${product.image}" alt="${product.name}">
          <div class="thumbs">
            ${[product.image, ...product.gallery].map((img) => `<button onclick="document.querySelector('#mainProductImage').src='${img}'"><img src="${img}" alt=""></button>`).join('')}
          </div>
        </div>
        <div>
          <p class="eyebrow">${product.category}</p>
          <h1 style="font-size:clamp(2.5rem,5vw,4.8rem);letter-spacing:-.055em">${product.name}</h1>
          <p class="muted">Star ${product.rating} · ${product.tag}</p>
          <p class="price" style="font-size:2rem">${money.format(product.price)}</p>
          <p class="lead">${product.description}</p>
          <p><strong>Finish</strong></p>
          <div class="row">${product.colors.map((color) => `<span class="tag">${color}</span>`).join('')}</div>
          <div class="actions" style="margin-top:28px">
            <button class="button-primary" onclick="addToCart('${product.id}')">Add to cart</button>
            <a class="button-primary" href="#payment/${product.id}">Buy now</a>
            <button class="button-secondary" onclick="toggleWishlist('${product.id}')">Wishlist</button>
          </div>
        </div>
      </section>
      <section class="section product-sections">
        <article class="panel product-detail-panel">
          <p class="eyebrow">Product Section</p>
          <h2>Why it stands out</h2>
          <div class="feature-list">${product.features.map((feature) => `<span>${feature}</span>`).join('')}</div>
        </article>
        <article class="panel product-detail-panel">
          <p class="eyebrow">Specifications</p>
          <h2>${product.name} details</h2>
          <dl class="spec-list">
            ${Object.entries(product.specs).map(([label, value]) => `<div><dt>${label}</dt><dd>${value}</dd></div>`).join('')}
          </dl>
        </article>
        <article class="panel product-detail-panel">
          <p class="eyebrow">Service</p>
          <h2>Included care</h2>
          <div class="feature-list">
            <span>30-day returns</span>
            <span>Premium protected packaging</span>
            <span>Two-year member support</span>
          </div>
        </article>
      </section>
      ${related.length ? `<section class="section"><div class="section-heading"><p class="eyebrow">Related</p><h2>More from ${product.category}</h2></div><div class="product-grid">${related.map(productCard).join('')}</div></section>` : ''}
    </div>
  `;
}

function cartPage() {
  const total = totals();
  if (!cart.length) {
    return `<section class="section empty page"><div class="empty-inner"><h1>Your cart is beautifully empty</h1><p class="muted">Add a few refined essentials and they will appear here.</p><a class="button-primary" href="#products">Start shopping</a></div></section>`;
  }
  return `
    <section class="section cart-layout page">
      <div><h1>Shopping cart</h1>${cart.map((item) => `
        <article class="cart-item">
          <img src="${item.image}" alt="${item.name}">
          <div><h3>${item.name}</h3><p class="muted">${item.category}</p><p class="price">${money.format(item.price)}</p></div>
          <div class="row">
            <button class="icon-button" onclick="setQuantity('${item.id}', 0)">Del</button>
            <div class="qty"><button onclick="setQuantity('${item.id}', ${item.quantity - 1})">-</button><span>${item.quantity}</span><button onclick="setQuantity('${item.id}', ${item.quantity + 1})">+</button></div>
          </div>
        </article>`).join('')}</div>
      ${summary(total, '<a class="button-primary" href="#payment/cart">Proceed to payment</a>')}
    </section>
  `;
}

function summary(total, action = '') {
  return `<aside class="panel" style="padding:24px;height:max-content"><h2>Order summary</h2><div class="summary-line"><span>Subtotal</span><strong>${money.format(total.subtotal)}</strong></div><div class="summary-line"><span>Shipping</span><strong>${money.format(total.shipping)}</strong></div><div class="summary-line"><span>Total</span><strong>${money.format(total.total)}</strong></div>${action}</aside>`;
}

function checkout() {
  if (!cart.length) {
    return `<section class="section empty page"><div class="empty-inner"><h1>Your cart needs one product first</h1><p class="muted">Choose a product or use Buy now for a single-item payment.</p><a class="button-primary" href="#products">Browse products</a></div></section>`;
  }

  return `
    <section class="section checkout-layout page">
      <form class="panel form-grid" style="padding:30px" onsubmit="event.preventDefault(); location.hash='payment/cart'">
        <p class="eyebrow">Checkout</p><h1>Delivery details</h1>
        <div class="form-grid two"><input class="input" placeholder="First name" required><input class="input" placeholder="Last name" required></div>
        <input class="input" type="email" placeholder="Email address" required>
        <input class="input" placeholder="Street address" required>
        <div class="form-grid three"><input class="input" placeholder="City" required><input class="input" placeholder="State" required><input class="input" placeholder="ZIP" required></div>
        <button class="button-primary">Continue to payment</button>
      </form>
      ${summary(totals())}
    </section>
  `;
}

function paymentItems(id) {
  if (id === 'cart') return cart;
  const product = products.find((item) => item.id === id);
  return product ? [{ ...product, quantity: 1 }] : [];
}

function paymentPage(id = 'cart') {
  const items = paymentItems(id);
  if (!items.length) {
    return `<section class="section empty page"><div class="empty-inner"><h1>No valid payment items</h1><p class="muted">That payment option is no longer available. Please choose a product again.</p><a class="button-primary" href="#products">Browse products</a></div></section>`;
  }

  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const shipping = 18;
  const total = subtotal + shipping;
  const clearCartAfterPayment = id === 'cart' ? "cart=[]; write('luxe-python-cart', cart); updateCartCount();" : '';

  return `
    <section class="section payment-layout page">
      <form class="panel form-grid payment-card" onsubmit="event.preventDefault(); ${clearCartAfterPayment} location.hash='success'; toast('Payment successful')">
        <p class="eyebrow">Payment Page</p>
        <h1>Complete payment</h1>
        <div class="payment-methods" role="group" aria-label="Payment method">
          <label><input type="radio" name="method" checked> Card</label>
          <label><input type="radio" name="method"> UPI</label>
          <label><input type="radio" name="method"> Wallet</label>
        </div>
        <input class="input" placeholder="Name on card" required>
        <input class="input" inputmode="numeric" placeholder="Card number" required>
        <div class="form-grid two">
          <input class="input" placeholder="MM / YY" required>
          <input class="input" inputmode="numeric" placeholder="CVC" required>
        </div>
        <input class="input" placeholder="Billing ZIP / PIN" required>
        <button class="button-primary">Pay ${money.format(total)}</button>
        <p class="muted">Demo payment only. No card details are stored or sent anywhere.</p>
      </form>
      <aside class="panel payment-summary">
        <p class="eyebrow">Order Review</p>
        <h2>${id === 'cart' ? 'Cart payment' : 'Buy now'}</h2>
        <div class="payment-items">
          ${items.map((item) => `
            <article>
              <img src="${item.image}" alt="${item.name}">
              <div>
                <h3>${item.name}</h3>
                <p class="muted">Qty ${item.quantity} - ${item.category}</p>
                <strong>${money.format(item.price * item.quantity)}</strong>
              </div>
            </article>
          `).join('')}
        </div>
        <div class="payment-total">
          <div><span>Subtotal</span><strong>${money.format(subtotal)}</strong></div>
          <div><span>Shipping</span><strong>${money.format(shipping)}</strong></div>
          <div><span>Total</span><strong>${money.format(total)}</strong></div>
        </div>
        <div class="payment-specs">
          <p class="eyebrow">Dedicated Specifications</p>
          ${items.map((item) => `
            <section>
              <h3>${item.name}</h3>
              <dl class="spec-list compact-specs">
                ${Object.entries(item.specs).map(([label, value]) => `<div><dt>${label}</dt><dd>${value}</dd></div>`).join('')}
              </dl>
            </section>
          `).join('')}
        </div>
      </aside>
    </section>
  `;
}

function auth() {
  return `
    <section class="section auth-layout page">
      <div>
        <p class="eyebrow">Member space</p>
        <h1>Your private atelier account.</h1>
        <p class="lead">Login to track orders, save wishlists, speed through checkout, and keep your premium picks close.</p>
        <div class="login-benefits">
          <div><strong>Order tracking</strong><span>Follow every delivery from confirmation to arrival.</span></div>
          <div><strong>Wishlist sync</strong><span>Keep your saved products available on every visit.</span></div>
          <div><strong>Faster checkout</strong><span>Store demo preferences locally for a smoother flow.</span></div>
        </div>
      </div>
      <div class="auth-stack">
        <form class="panel form-grid auth-card" onsubmit="event.preventDefault(); toast('Logged in successfully')">
          <p class="eyebrow">Login</p>
          <h2>Welcome back</h2>
          <input class="input" type="email" placeholder="Email address" required>
          <input class="input" type="password" placeholder="Password" required>
          <div class="row" style="justify-content:space-between">
            <label class="check"><input type="checkbox"> Remember me</label>
            <button class="link-button" type="button" onclick="toast('Password reset link sent')">Forgot password?</button>
          </div>
          <button class="button-primary">Login</button>
        </form>
        <form class="panel form-grid auth-card" onsubmit="event.preventDefault(); toast('Account created')">
          <p class="eyebrow">Register</p>
          <h2>Create account</h2>
          <input class="input" placeholder="Full name" required>
          <input class="input" type="email" placeholder="Email address" required>
          <input class="input" type="password" placeholder="Create password" required>
          <button class="button-secondary">Register</button>
        </form>
      </div>
    </section>
  `;
}

function profile() {
  const total = totals();
  return `<section class="section page"><p class="eyebrow">Dashboard</p><h1>Welcome, Atelier Member</h1><div class="dashboard-grid grid-3"><div class="card"><p class="muted">Cart value</p><h2>${money.format(total.total)}</h2></div><div class="card"><p class="muted">Wishlist items</p><h2>${wishlist.length}</h2></div><div class="card"><p class="muted">Member tier</p><h2>Black</h2></div></div><div class="grid-3" style="margin-top:22px"><div class="card"><h2>Recent orders</h2><p>LA-2048 · Processing</p><p>LA-1982 · Delivered</p><p>LA-1844 · Delivered</p></div><div class="card"><h2>Saved cart</h2>${cart.map((item) => `<p>${item.name} · Qty ${item.quantity}</p>`).join('') || '<p class="muted">No active cart items.</p>'}</div></div></section>`;
}

function wishlistPage() {
  return wishlist.length
    ? `<section class="section page"><p class="eyebrow">Saved</p><h1>Wishlist</h1><div class="product-grid">${wishlist.map(productCard).join('')}</div></section>`
    : `<section class="section empty page"><div class="empty-inner"><h1>No saved pieces yet</h1><p class="muted">Tap the heart on any product to keep it close.</p><a class="button-primary" href="#products">Browse products</a></div></section>`;
}

function success() {
  return `<section class="section empty page"><div class="empty-inner panel" style="padding:42px"><h1>Your essentials are on their way.</h1><p class="muted">A confirmation has been simulated for this demo checkout. Your order number is LA-2056.</p><a class="button-primary" href="#products">Continue shopping</a></div></section>`;
}

function notFound() {
  return `<section class="section empty page"><div><h1>404</h1><p class="muted">This page is not part of the collection.</p><a class="button-primary" href="#home">Return home</a></div></section>`;
}

function bindProductsFilters() {
  const search = document.querySelector('#pageSearch');
  const category = document.querySelector('#categoryFilter');
  const sort = document.querySelector('#sortFilter');
  const grid = document.querySelector('#productGrid');
  if (!search || !category || !sort || !grid) return;

  const update = () => {
    let list = products.filter((item) => category.value === 'All' || item.category === category.value);
    list = list.filter((item) => `${item.name} ${item.description}`.toLowerCase().includes(search.value.toLowerCase()));
    list.sort((a, b) => {
      if (sort.value === 'low') return a.price - b.price;
      if (sort.value === 'high') return b.price - a.price;
      if (sort.value === 'rating') return b.rating - a.rating;
      return 0;
    });
    grid.innerHTML = list.map(productCard).join('') || '<div class="panel empty"><div><h2>No products found</h2><p class="muted">Try another category or search term.</p></div></div>';
  };

  search.addEventListener('input', update);
  category.addEventListener('change', update);
  sort.addEventListener('change', update);
}

function render() {
  const route = location.hash.replace(/^#/, '') || 'home';
  const [path] = route.split('?');
  const [name, id] = path.split('/');
  app.innerHTML = {
    home,
    products: productsPage,
    cart: cartPage,
    checkout,
    payment: () => paymentPage(id || 'cart'),
    auth,
    login: auth,
    profile,
    wishlist: wishlistPage,
    success,
  }[name]?.() || (name === 'product' ? productDetails(id) : notFound());
  bindProductsFilters();
  scrollTo({ top: 0, behavior: 'smooth' });
}

document.querySelector('#themeToggle').addEventListener('click', () => {
  theme = theme === 'dark' ? 'light' : 'dark';
  updateTheme();
});

document.querySelector('#menuToggle').addEventListener('click', () => {
  document.querySelector('#mobileMenu').classList.toggle('open');
});

document.querySelector('#navSearch').addEventListener('submit', (event) => {
  event.preventDefault();
  const value = document.querySelector('#searchInput').value.trim();
  location.hash = `products${value ? `?search=${encodeURIComponent(value)}` : ''}`;
});

addEventListener('hashchange', render);
addEventListener('load', () => {
  updateTheme();
  updateCartCount();
  render();
  setTimeout(() => document.querySelector('#loading').classList.add('hidden'), 450);
});
