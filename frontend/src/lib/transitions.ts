export function withTransition(fn: () => void) {
  if ('startViewTransition' in document) {
    document.startViewTransition(fn);
  } else {
    fn();
  }
}
