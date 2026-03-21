<script lang="ts">
  import type { ProductosPorCategoria } from '../../types/index.js';
  import ProductCard from './ProductCard.svelte';

  interface Props {
    group: ProductosPorCategoria;
  }

  let { group }: Props = $props();
</script>

<section class="mb-16">
  <div class="flex items-baseline justify-between mb-6">
    <h2 class="text-2xl font-semibold" style="color: var(--color-foreground);">
      {group.categoria.nombre}
    </h2>
    {#if group.productos.length > 3}
      <a
        href={`/#/products?categoria=${group.categoria.slug}`}
        class="text-sm transition-opacity hover:opacity-70"
        style="color: var(--color-primary);"
      >
        Ver todos
      </a>
    {/if}
  </div>

  <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
    {#each group.productos as product (product._id)}
      <ProductCard {product} />
    {/each}
  </div>
</section>
