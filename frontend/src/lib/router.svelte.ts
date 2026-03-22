import { flushSync } from 'svelte';

let _location = $state(typeof window !== 'undefined' ? window.location.pathname : '/');

if (typeof window !== 'undefined') {
  history.scrollRestoration = 'manual';

  window.addEventListener('popstate', (e) => {
    const savedY = (e.state as { scrollY?: number } | null)?.scrollY ?? 0;
    if ('startViewTransition' in document) {
      (document as Document & { startViewTransition(fn: () => void): void }).startViewTransition(
        () => {
          flushSync(() => {
            _location = window.location.pathname;
          });
          window.scrollTo({ top: savedY, behavior: 'instant' });
        }
      );
    } else {
      _location = window.location.pathname;
      window.scrollTo({ top: savedY, behavior: 'instant' });
    }
  });
}

export const router = {
  get location() {
    return _location;
  },
};

export function push(path: string) {
  history.replaceState({ scrollY: window.scrollY }, '');
  history.pushState({ scrollY: 0 }, '', path);
  _location = path;
  window.scrollTo({ top: 0, behavior: 'instant' });
}
