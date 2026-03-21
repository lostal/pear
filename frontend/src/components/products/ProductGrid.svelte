<script lang="ts">
  import type { Product } from '../../types/index.js';
  import ProductCard from './ProductCard.svelte';
  import ProductCardSkeleton from './ProductCardSkeleton.svelte';

  interface Props {
    products: Product[];
    loading?: boolean;
    onEdit?: (product: Product) => void;
    onDelete?: (product: Product) => void;
    onView?: (product: Product) => void;
  }

  let { products, loading = false, onEdit, onDelete, onView }: Props = $props();
</script>

{#if loading}
  <div class="divide-y divide-[var(--color-border)]">
    {#each Array(5) as _}
      <ProductCardSkeleton />
    {/each}
  </div>
{:else if products.length === 0}
  <div class="text-center py-20 text-[var(--color-muted-foreground)]">
    <p class="text-4xl mb-3">🍐</p>
    <p class="text-lg font-medium">No hay productos</p>
    <p class="text-sm">Prueba a cambiar los filtros o crea uno nuevo.</p>
  </div>
{:else}
  <div class="divide-y divide-[var(--color-border)]">
    {#each products as product (product._id)}
      <ProductCard {product} {onEdit} {onDelete} {onView} />
    {/each}
  </div>
{/if}
