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
    success: 'border-l-[var(--color-apple-blue)] bg-blue-50',
    error: 'border-l-[var(--color-destructive)] bg-red-50',
    info: 'border-l-blue-500 bg-blue-50',
    warning: 'border-l-amber-500 bg-amber-50',
  };

  const iconColors: Record<string, string> = {
    success: 'color: var(--color-apple-blue);',
    error: 'color: var(--color-destructive);',
    info: 'color: #3b82f6;',
    warning: 'color: #f59e0b;',
  };
</script>

<div
  class="flex items-start gap-3 px-4 py-3 rounded-2xl border-l-4 min-w-[280px] max-w-sm bg-white {colors[item.type]}"
  style="box-shadow: 0 4px 16px rgba(0,0,0,0.1);"
  role="alert"
>
  <span class="font-semibold text-sm mt-0.5" style={iconColors[item.type]}>{icons[item.type]}</span>
  <p class="flex-1 text-sm" style="color: var(--color-foreground);">{item.message}</p>
  <button
    onclick={() => toast.remove(item.id)}
    class="transition-colors text-xs cursor-pointer"
    style="color: var(--color-muted-foreground);"
    aria-label="Cerrar"
  >✕</button>
</div>
