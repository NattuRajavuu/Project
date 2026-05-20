import { Link } from 'react-router-dom';
import PageShell from '../components/PageShell';

export default function NotFound() {
  return (
    <PageShell>
      <section className="section grid min-h-[55vh] place-items-center text-center">
        <div>
          <h1 className="text-5xl font-extrabold">404</h1>
          <p className="mt-3 text-black/55 dark:text-white/55">This page is not part of the collection.</p>
          <Link className="button-primary mt-6" to="/">Return home</Link>
        </div>
      </section>
    </PageShell>
  );
}
