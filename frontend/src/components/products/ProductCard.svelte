<script lang="ts">
  import type { Product } from '../../types/index.js';
  import { auth } from '../../stores/auth.svelte.js';
  import { push } from 'svelte-spa-router';

  interface Props {
    product: Product;
    onEdit?: (product: Product) => void;
    onDelete?: (product: Product) => void;
    onView?: (product: Product) => void;
  }

  let { product, onEdit, onDelete, onView }: Props = $props();

  const initial = $derived(product.nombre.charAt(0).toUpperCase());

  function formatPrice(price: number) {
    return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(price);
  }

  function handleClick() {
    if (onView) {
      onView(product);
    } else {
      push(`/products/${product._id}`);
    }
  }
</script>

<article
  class="group relative bg-card rounded-lg border border-border overflow-hidden cursor-pointer transition-all duration-200 hover:shadow-md"
  style="opacity:0;"
>
  <!-- Imagen o placeholder con inicial -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="aspect-square flex items-center justify-center overflow-hidden"
    style="background: var(--color-secondary);"
    onclick={handleClick}
  >
    {#if product.imagen}
      <img
        src="/api/uploads/{product.imagen}"
        alt={product.nombre}
        class="w-full h-full object-cover"
      />
    {:else}
      <span
        class="text-5xl font-black select-none"
        style="color: var(--color-border); line-height: 1;"
      >
        {initial}
      </span>
    {/if}
  </div>

  <!-- Info -->
  <div class="p-4">
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div onclick={handleClick}>
      <h2 class="font-medium text-sm leading-snug mb-1" style="color: var(--color-foreground);">
        {product.nombre}
      </h2>
      <p class="text-sm" style="color: var(--color-muted-foreground);">
        {formatPrice(product.precio)}
      </p>
    </div>

    {#if auth.isAdmin}
      <div class="mt-3 flex gap-4 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
        <button
          onclick={(e) => { e.stopPropagation(); onEdit?.(product); }}
          class="text-xs transition-colors cursor-pointer hover:opacity-100 opacity-70"
          style="color: var(--color-foreground);"
        >
          Editar
        </button>
        <button
          onclick={(e) => { e.stopPropagation(); onDelete?.(product); }}
          class="text-xs transition-colors cursor-pointer"
          style="color: var(--color-destructive);"
        >
          Eliminar
        </button>
      </div>
    {/if}
  </div>
</article>
