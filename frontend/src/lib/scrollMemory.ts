const memory: Record<string, number> = {};

export function saveScroll(path: string) {
  memory[path] = window.scrollY;
}

export function restoreScroll(path: string): number {
  return memory[path] ?? 0;
}
