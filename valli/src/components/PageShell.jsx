import { motion } from 'framer-motion';
import { pageTransition } from '../animations/variants';

export default function PageShell({ children, className = '' }) {
  return (
    <motion.div {...pageTransition} className={`min-h-[70vh] py-10 sm:py-14 ${className}`}>
      {children}
    </motion.div>
  );
}
