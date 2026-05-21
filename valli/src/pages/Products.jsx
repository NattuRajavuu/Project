import { SlidersHorizontal } from 'lucide-react';
import { motion } from 'framer-motion';
import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { stagger } from '../animations/variants';
import PageShell from '../components/PageShell';
import ProductCard from '../components/ProductCard';
import SectionHeading from '../components/SectionHeading';
import SkeletonGrid from '../components/SkeletonGrid';
import { categories, products } from '../data/products';
import { fetchProducts } from '../utils/api';

export default function Products() {
  const [params, setParams] = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState(params.get('category') || 'All');
  const [search, setSearch] = useState(params.get('search') || '');
  const [sort, setSort] = useState('featured');
  const [apiProducts, setApiProducts] = useState(products);

  useEffect(() => {
    let active = true;
    let timer;
    setLoading(true);

    fetchProducts({ search, category, sort })
      .then((data) => {
        if (active) setApiProducts(data.products || []);
      })
      .catch(() => {
        if (active) setApiProducts(products);
      })
      .finally(() => {
        if (active) timer = setTimeout(() => setLoading(false), 350);
      });

    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [category, search, sort]);

  useEffect(() => {
    const next = {};
    if (category !== 'All') next.category = category;
    if (search) next.search = search;
    setParams(next, { replace: true });
  }, [category, search, setParams]);

  const filtered = useMemo(() => {
    const result = apiProducts
      .filter((product) => category === 'All' || product.category === category)
      .filter((product) => product.name.toLowerCase().includes(search.toLowerCase()) || product.description.toLowerCase().includes(search.toLowerCase()));

    return [...result].sort((a, b) => {
      if (sort === 'low') return a.price - b.price;
      if (sort === 'high') return b.price - a.price;
      if (sort === 'rating') return b.rating - a.rating;
      return 0;
    });
  }, [apiProducts, category, search, sort]);

  return (
    <PageShell>
      <section className="section">
        <SectionHeading eyebrow="The Collection" title="Shop refined essentials" text="Filter by category, search by need, and sort the collection your way." />
        <div className="glass mb-8 grid gap-4 rounded-[2rem] p-4 lg:grid-cols-[1fr_auto_auto]">
          <input className="input" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search products" />
          <select className="input lg:w-52" value={category} onChange={(event) => setCategory(event.target.value)} aria-label="Filter category">
            {categories.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
          <select className="input lg:w-52" value={sort} onChange={(event) => setSort(event.target.value)} aria-label="Sort products">
            <option value="featured">Featured</option>
            <option value="low">Price: Low to High</option>
            <option value="high">Price: High to Low</option>
            <option value="rating">Top Rated</option>
          </select>
        </div>
        <div className="mb-5 flex items-center gap-2 text-sm font-semibold text-black/55 dark:text-white/55">
          <SlidersHorizontal className="h-4 w-4" /> {filtered.length} products
        </div>
        {loading ? (
          <SkeletonGrid />
        ) : filtered.length ? (
          <motion.div initial="hidden" animate="visible" variants={stagger} className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </motion.div>
        ) : (
          <div className="rounded-[2rem] border border-black/10 bg-white p-10 text-center dark:border-white/10 dark:bg-white/10">
            <h3 className="text-xl font-bold">No products found</h3>
            <p className="mt-2 text-sm text-black/55 dark:text-white/55">Try another category or search term.</p>
          </div>
        )}
      </section>
    </PageShell>
  );
}
