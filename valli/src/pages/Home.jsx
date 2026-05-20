import { ArrowRight, Gem, ShieldCheck, Sparkles, Truck } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { fadeUp, stagger } from '../animations/variants';
import Newsletter from '../components/Newsletter';
import PageShell from '../components/PageShell';
import ProductCard from '../components/ProductCard';
import SectionHeading from '../components/SectionHeading';
import { products, testimonials } from '../data/products';

const categories = [
  { name: 'Audio', image: products[0].image },
  { name: 'Wearables', image: products[1].image },
  { name: 'Home', image: products[2].image },
];

export default function Home() {
  return (
    <PageShell className="pt-0">
      <section className="section grid min-h-[calc(100vh-5rem)] items-center gap-10 py-12 lg:grid-cols-[1fr_0.9fr]">
        <motion.div initial="hidden" animate="visible" variants={stagger}>
          <motion.p variants={fadeUp} className="text-xs font-extrabold uppercase tracking-[0.3em] text-black/45 dark:text-white/45">
            Minimal luxury objects
          </motion.p>
          <motion.h1 variants={fadeUp} className="mt-5 max-w-3xl text-5xl font-extrabold leading-[0.95] tracking-tight sm:text-6xl lg:text-7xl">
            Designed essentials for a calmer everyday.
          </motion.h1>
          <motion.p variants={fadeUp} className="mt-6 max-w-xl text-base leading-7 text-black/60 dark:text-white/60">
            Premium technology, refined home pieces, and travel accessories curated with quiet confidence.
          </motion.p>
          <motion.div variants={fadeUp} className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link className="button-primary" to="/products">
              Shop collection <ArrowRight className="h-4 w-4" />
            </Link>
            <Link className="button-secondary" to="/wishlist">
              View wishlist
            </Link>
          </motion.div>
        </motion.div>
        <motion.div initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.8 }} className="relative">
          <div className="absolute inset-5 rounded-[3rem] bg-black/10 blur-3xl dark:bg-white/10" />
          <img
            src="https://images.unsplash.com/photo-1491933382434-500287f9b54b?auto=format&fit=crop&w=1400&q=85"
            alt="Premium desk setup"
            className="relative aspect-[4/5] w-full rounded-[2.5rem] object-cover shadow-glow"
          />
          <div className="glass absolute bottom-5 left-5 right-5 rounded-[1.5rem] p-4">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.2em] text-black/45 dark:text-white/45">Featured</p>
                <p className="mt-1 font-bold">Monolith Speaker</p>
              </div>
              <span className="rounded-full bg-ink px-4 py-2 text-sm font-bold text-white dark:bg-white dark:text-ink">$680</span>
            </div>
          </div>
        </motion.div>
      </section>

      <section className="section py-12">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            [Truck, 'Express Delivery', 'Fast, tracked shipping worldwide.'],
            [ShieldCheck, 'Secure Checkout', 'Protected payments and privacy.'],
            [Gem, 'Premium Curation', 'Only objects worth owning.'],
            [Sparkles, 'Member Access', 'Early drops and private edits.'],
          ].map(([Icon, title, text]) => (
            <div key={title} className="rounded-[1.5rem] border border-black/10 bg-white p-5 shadow-soft dark:border-white/10 dark:bg-white/10">
              <Icon className="h-5 w-5" />
              <h3 className="mt-4 font-bold">{title}</h3>
              <p className="mt-2 text-sm leading-6 text-black/55 dark:text-white/55">{text}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="section py-16">
        <SectionHeading eyebrow="Shop by mood" title="Category edits" text="Focused collections for sound, work, home, and motion." />
        <div className="grid gap-5 md:grid-cols-3">
          {categories.map((category) => (
            <Link key={category.name} to={`/products?category=${category.name}`} className="group relative overflow-hidden rounded-[2rem]">
              <img src={category.image} alt={category.name} className="aspect-[4/3] w-full object-cover transition duration-700 group-hover:scale-105" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/55 to-transparent" />
              <div className="absolute bottom-5 left-5 text-white">
                <p className="text-2xl font-extrabold">{category.name}</p>
                <p className="mt-1 text-sm opacity-75">Explore edit</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="section py-16">
        <SectionHeading eyebrow="Featured" title="Objects with presence" text="Premium pieces chosen for performance, silhouette, and daily usefulness." />
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, margin: '-80px' }} variants={stagger} className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {products.slice(0, 3).map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </motion.div>
      </section>

      <section className="section py-16">
        <SectionHeading eyebrow="Notes" title="Loved by detail people" />
        <div className="grid gap-5 md:grid-cols-3">
          {testimonials.map((item) => (
            <blockquote key={item.name} className="rounded-[1.5rem] border border-black/10 bg-white p-6 shadow-soft dark:border-white/10 dark:bg-white/10">
              <p className="leading-7 text-black/70 dark:text-white/70">"{item.text}"</p>
              <footer className="mt-5 text-sm font-bold">{item.name}</footer>
            </blockquote>
          ))}
        </div>
      </section>
      <Newsletter />
    </PageShell>
  );
}
