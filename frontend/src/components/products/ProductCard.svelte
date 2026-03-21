<script lang="ts">
  import type { Product } from '../../types/index.js';
  import { auth } from '../../stores/auth.svelte.js';
  import Button from '../ui/Button.svelte';

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

<div class="flex flex-col bg-[var(--color-card)] border border-[var(--color-border)] rounded-lg p-4 gap-3 hover:shadow-md transition-shadow">
  <button
    onclick={() => onView?.(product)}
    class="text-left font-semibold leading-tight hover:text-[var(--color-pear)] transition-colors cursor-pointer"
  >
    {product.nombre}
  </button>

  <div class="flex items-center justify-between mt-auto pt-2 border-t border-[var(--color-border)]">
    <span class="font-bold text-lg">{formatPrice(product.precio)}</span>

    {#if auth.isAdmin}
      <div class="flex gap-2">
        <Button size="sm" variant="secondary" onclick={() => onEdit?.(product)}>Editar</Button>
        <Button size="sm" variant="destructive" onclick={() => onDelete?.(product)}>Borrar</Button>
      </div>
    {/if}
  </div>
</div>
