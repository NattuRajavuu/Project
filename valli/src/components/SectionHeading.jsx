export default function SectionHeading({ eyebrow, title, text }) {
  return (
    <div className="mx-auto mb-10 max-w-2xl text-center">
      {eyebrow && <p className="mb-3 text-xs font-extrabold uppercase tracking-[0.25em] text-black/45 dark:text-white/45">{eyebrow}</p>}
      <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl">{title}</h2>
      {text && <p className="mt-4 text-sm leading-6 text-black/55 dark:text-white/55 sm:text-base">{text}</p>}
    </div>
  );
}
