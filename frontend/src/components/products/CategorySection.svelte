<script lang="ts">
  import type { ProductosPorCategoria } from '../../types/index.js';
  import ProductCard from './ProductCard.svelte';
  import { ArrowRight } from 'lucide-svelte';
  import { push } from '../../lib/router.svelte.js';
  import { withTransition } from '../../lib/transitions.js';

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
      <button
        onclick={() => withTransition(() => push('/products'))}
        class="text-sm flex items-center gap-1 transition-opacity hover:opacity-70 group cursor-pointer"
        style="color: var(--color-muted-foreground);"
      >
        Ver todos
        <ArrowRight size={14} class="transition-transform group-hover:translate-x-0.5" />
      </button>
    {/if}
  </div>

  <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
    {#each group.productos as product (product._id)}
      <ProductCard {product} />
    {/each}
  </div>
</section>
