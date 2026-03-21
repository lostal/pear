<script lang="ts">
  import type { Product } from '../../types/index.js';
  import { auth } from '../../stores/auth.svelte.js';

  interface Props {
    product: Product;
    onEdit?: (product: Product) => void;
    onDelete?: (product: Product) => void;
    onView?: (product: Product) => void;
  }

  let { product, onEdit, onDelete, onView }: Props = $props();

  function formatPrice(price: number) {
    return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(price);
  }
</script>

<article class="group relative -mx-4 px-4 py-5 sm:py-6 rounded-2xl hover:bg-[var(--color-accent)] transition-all duration-300">
  <!-- Clickable overlay -->
  <!-- svelte-ignore a11y_interactive_supports_focus -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    role="button"
    onclick={() => onView?.(product)}
    class="absolute inset-0 z-10 cursor-pointer rounded-2xl"
  ></div>

  <div class="flex items-start justify-between gap-6">
    <!-- Left: name + admin actions -->
    <div class="flex-1 min-w-0">
      <h2 class="text-xl sm:text-2xl font-black tracking-tight leading-tight text-[var(--color-foreground)] group-hover:text-[var(--color-primary)] transition-colors">
        {product.nombre}
      </h2>
      {#if auth.isAdmin}
        <div class="mt-2.5 flex items-center gap-5 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <button
            onclick={(e) => { e.stopPropagation(); onEdit?.(product); }}
            class="relative z-20 text-xs font-bold uppercase tracking-widest text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)] transition-colors cursor-pointer"
          >
            Editar
          </button>
          <button
            onclick={(e) => { e.stopPropagation(); onDelete?.(product); }}
            class="relative z-20 text-xs font-bold uppercase tracking-widest text-[var(--color-muted-foreground)] hover:text-[var(--color-destructive)] transition-colors cursor-pointer"
          >
            Eliminar
          </button>
        </div>
      {/if}
    </div>
    <!-- Right: price in large serif -->
    <span class="font-serif text-3xl sm:text-4xl text-[var(--color-foreground)] flex-shrink-0 tabular-nums">
      {formatPrice(product.precio)}
    </span>
  </div>
</article>
