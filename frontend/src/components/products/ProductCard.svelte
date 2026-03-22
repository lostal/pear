<script lang="ts">
  import type { Product } from '../../types/index.js';
  import { getImagenesForProduct, getPrecioMinimo, getImageUrl } from '../../types/index.js';
  import { push } from '../../lib/router.svelte.js';
  import { withTransition } from '../../lib/transitions.js';
  import { saveScroll } from '../../lib/scrollMemory.js';
  import { formatPrice } from '../../lib/utils.js';

  interface Props {
    product: Product;
  }

  let { product }: Props = $props();

  const initial = $derived(product.nombre.charAt(0).toUpperCase());
  const imagenes = $derived(getImagenesForProduct(product));
  const precio = $derived(getPrecioMinimo(product));
  const colorGrupo = $derived(product.gruposOpciones.find((g) => g.tipo === 'color'));


</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<article
  class="group cursor-pointer"
  onclick={() => { saveScroll('/products'); withTransition(() => push(`/products/${product._id}`)); }}
>
  <!-- Imagen -->
  <div
    class="aspect-square rounded-2xl overflow-hidden flex items-center justify-center mb-3 transition-transform duration-300 group-hover:scale-[1.02]"
    style="background: var(--color-secondary); view-transition-name: product-image-{product._id};"
  >
    {#if imagenes.length > 0}
      <img src={getImageUrl(imagenes[0])} alt={product.nombre} class="w-full h-full object-cover" />
    {:else}
      <span class="text-5xl font-black select-none" style="color: var(--color-border);">
        {initial}
      </span>
    {/if}
  </div>

  <!-- Info -->
  <div class="px-1">
    <h3
      class="text-sm font-medium leading-snug mb-1"
      style="color: var(--color-foreground); view-transition-name: product-title-{product._id};"
    >
      {product.nombre}
    </h3>

    <!-- Swatches de color -->
    {#if colorGrupo && colorGrupo.opciones.length > 0}
      <div class="flex gap-1 mb-1">
        {#each colorGrupo.opciones.slice(0, 8) as opcion}
          <span
            class="w-3 h-3 rounded-full border border-black/10"
            style="background: {opcion.codigoHex ?? '#ccc'};"
            title={opcion.valor}
          ></span>
        {/each}
      </div>
    {/if}

    <p class="text-xs" style="color: var(--color-muted-foreground);">
      Desde {formatPrice(precio)}
    </p>
  </div>
</article>
