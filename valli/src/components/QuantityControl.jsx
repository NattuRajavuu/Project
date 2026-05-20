import { Minus, Plus } from 'lucide-react';

export default function QuantityControl({ value, onChange }) {
  return (
    <div className="inline-flex h-11 items-center rounded-full border border-black/10 bg-white dark:border-white/10 dark:bg-white/10">
      <button className="grid h-11 w-11 place-items-center" onClick={() => onChange(value - 1)} aria-label="Decrease quantity">
        <Minus className="h-4 w-4" />
      </button>
      <span className="w-8 text-center text-sm font-bold">{value}</span>
      <button className="grid h-11 w-11 place-items-center" onClick={() => onChange(value + 1)} aria-label="Increase quantity">
        <Plus className="h-4 w-4" />
      </button>
    </div>
  );
}
