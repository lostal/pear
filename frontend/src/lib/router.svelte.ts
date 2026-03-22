import { flushSync } from 'svelte';

let _location = $state(typeof window !== 'undefined' ? window.location.pathname : '/');

if (typeof window !== 'undefined') {
  window.addEventListener('popstate', () => {
    if ('startViewTransition' in document) {
      (document as Document & { startViewTransition(fn: () => void): void }).startViewTransition(
        () => {
          flushSync(() => {
            _location = window.location.pathname;
          });
        }
      );
    } else {
      _location = window.location.pathname;
    }
  });
}

export const router = {
  get location() {
    return _location;
  },
};

export function push(path: string) {
  history.pushState(null, '', path);
  _location = path;
}
