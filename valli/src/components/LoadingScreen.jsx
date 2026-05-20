import { motion } from 'framer-motion';

export default function LoadingScreen() {
  return (
    <div className="grid min-h-screen place-items-center bg-pearl text-ink dark:bg-ink dark:text-white">
      <div className="text-center">
        <motion.div
          className="mx-auto h-16 w-16 rounded-full border border-black/10 bg-white shadow-soft dark:border-white/10 dark:bg-white/10"
          animate={{ scale: [1, 1.08, 1], opacity: [0.75, 1, 0.75] }}
          transition={{ duration: 1.1, repeat: Infinity, ease: 'easeInOut' }}
        />
        <p className="mt-5 text-xs font-extrabold uppercase tracking-[0.3em] text-black/45 dark:text-white/45">Luxe Atelier</p>
      </div>
    </div>
  );
}
