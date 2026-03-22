import { flushSync } from 'svelte';

export function withTransition(fn: () => void) {
  if (!('startViewTransition' in document)) {
    fn();
    return;
  }
  document.startViewTransition(() => {
    flushSync(fn);
    window.scrollTo({ top: 0, behavior: 'instant' });
  });
}
