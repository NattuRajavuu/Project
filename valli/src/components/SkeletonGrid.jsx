export default function SkeletonGrid() {
  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: 6 }).map((_, index) => (
        <div key={index} className="overflow-hidden rounded-[2rem] border border-black/10 bg-white p-4 dark:border-white/10 dark:bg-white/10">
          <div className="h-56 animate-pulse rounded-[1.5rem] bg-black/10 dark:bg-white/10" />
          <div className="mt-5 h-4 w-1/2 animate-pulse rounded bg-black/10 dark:bg-white/10" />
          <div className="mt-3 h-4 w-3/4 animate-pulse rounded bg-black/10 dark:bg-white/10" />
          <div className="mt-6 h-10 w-full animate-pulse rounded-full bg-black/10 dark:bg-white/10" />
        </div>
      ))}
    </div>
  );
}
