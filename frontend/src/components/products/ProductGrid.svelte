<script lang="ts">
  import { animate, stagger } from 'motion';
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

  let gridEl: HTMLElement | undefined = $state();

  $effect(() => {
    if (!loading && products.length > 0 && gridEl) {
      const cards = gridEl.querySelectorAll('article');
      animate(
        cards,
        { opacity: [0, 1], y: [20, 0] },
        { delay: stagger(0.06), duration: 0.4, easing: [0.25, 0.1, 0.25, 1] }
      );
    }
  });
</script>

{#if loading}
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
    {#each Array(6) as _}
      <ProductCardSkeleton />
    {/each}
  </div>
{:else if products.length === 0}
  <div class="text-center py-20">
    <p class="text-lg font-medium" style="color: var(--color-muted-foreground);">
      No hay productos
    </p>
    <p class="text-sm mt-1" style="color: var(--color-muted-foreground); opacity: 0.6;">
      Prueba a cambiar los filtros o crea uno nuevo.
    </p>
  </div>
{:else}
  <div
    bind:this={gridEl}
    class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5"
  >
    {#each products as product (product._id)}
      <ProductCard {product} {onEdit} {onDelete} {onView} />
    {/each}
  </div>
{/if}
