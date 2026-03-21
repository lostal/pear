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
    info: 'i',
    warning: '!',
  };

  const borderColors: Record<string, string> = {
    success: 'var(--color-primary)',
    error: 'var(--color-destructive)',
    info: 'var(--color-border)',
    warning: '#d97706',
  };

  const iconColors: Record<string, string> = {
    success: 'var(--color-foreground)',
    error: 'var(--color-destructive)',
    info: 'var(--color-muted-foreground)',
    warning: '#d97706',
  };
</script>

<div
  class="flex items-start gap-3 px-4 py-3 rounded-lg border-l-4 min-w-70 max-w-sm border"
  style="background: var(--color-card); border-color: var(--color-border); border-left-color: {borderColors[item.type]}; box-shadow: 0 4px 16px rgba(0,0,0,0.08);"
  role="alert"
>
  <span
    class="font-black text-xs mt-0.5 w-4 h-4 flex items-center justify-center shrink-0"
    style="color: {iconColors[item.type]};"
  >{icons[item.type]}</span>
  <p class="flex-1 text-sm" style="color: var(--color-foreground);">{item.message}</p>
  <button
    onclick={() => toast.remove(item.id)}
    class="transition-opacity text-xs cursor-pointer hover:opacity-100 opacity-50 shrink-0"
    style="color: var(--color-foreground);"
    aria-label="Cerrar"
  >✕</button>
</div>
