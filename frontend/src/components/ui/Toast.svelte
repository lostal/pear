<script lang="ts">
  import type { Toast as ToastItem } from '../../stores/toast.svelte.js';
  import { toast } from '../../stores/toast.svelte.js';

  interface Props {
    item: ToastItem;
  }

  let { item }: Props = $props();

  const icons: Record<string, string> = {
    success: '✓',
    error: '✕',
    info: 'ℹ',
    warning: '⚠',
  };

  const colors: Record<string, string> = {
    success: 'border-l-[var(--color-pear)] bg-[var(--color-pear-muted)]',
    error: 'border-l-[var(--color-destructive)] bg-red-50 dark:bg-red-900/10',
    info: 'border-l-blue-500 bg-blue-50 dark:bg-blue-900/10',
    warning: 'border-l-amber-500 bg-amber-50 dark:bg-amber-900/10',
  };

  const iconColors: Record<string, string> = {
    success: 'text-[var(--color-pear)]',
    error: 'text-[var(--color-destructive)]',
    info: 'text-blue-600',
    warning: 'text-amber-600',
  };
</script>

<div
  class="flex items-start gap-3 px-4 py-3 rounded-md border-l-4 shadow-md min-w-[280px] max-w-sm {colors[item.type]} bg-[var(--color-card)]"
  role="alert"
>
  <span class="font-bold text-sm mt-0.5 {iconColors[item.type]}">{icons[item.type]}</span>
  <p class="flex-1 text-sm text-[var(--color-foreground)]">{item.message}</p>
  <button
    onclick={() => toast.remove(item.id)}
    class="text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)] transition-colors text-xs"
    aria-label="Cerrar"
  >✕</button>
</div>
