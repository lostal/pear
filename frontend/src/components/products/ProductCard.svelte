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

  const GRADIENTS = [
    'linear-gradient(135deg, #e8f4fd 0%, #bee3f8 100%)',
    'linear-gradient(135deg, #f0e8fd 0%, #e9d8fd 100%)',
    'linear-gradient(135deg, #e8fdf0 0%, #c6f6d5 100%)',
    'linear-gradient(135deg, #fdf3e8 0%, #fde8c8 100%)',
    'linear-gradient(135deg, #fde8f4 0%, #fed7e2 100%)',
    'linear-gradient(135deg, #fdfbe8 0%, #fef9c3 100%)',
  ];

  const gradient = $derived(GRADIENTS[product.nombre.charCodeAt(0) % 6]);

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
  class="group relative bg-white rounded-2xl overflow-hidden cursor-pointer"
  style="opacity:0; box-shadow: 0 2px 8px rgba(0,0,0,0.06); transition: transform 0.2s ease, box-shadow 0.2s ease;"
  onmouseenter={(e) => { (e.currentTarget as HTMLElement).style.transform = 'translateY(-4px)'; (e.currentTarget as HTMLElement).style.boxShadow = '0 8px 24px rgba(0,0,0,0.12)'; }}
  onmouseleave={(e) => { (e.currentTarget as HTMLElement).style.transform = 'translateY(0)'; (e.currentTarget as HTMLElement).style.boxShadow = '0 2px 8px rgba(0,0,0,0.06)'; }}
>
  <!-- Image zone: aspect-square gradient or real image -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="aspect-square flex items-center justify-center text-5xl"
    style="background: {gradient};"
    onclick={handleClick}
  >
    {#if product.imagen}
      <img
        src="/api/uploads/{product.imagen}"
        alt={product.nombre}
        class="w-full h-full object-cover"
      />
    {:else}
      🍐
    {/if}
  </div>

  <!-- Info zone -->
  <div class="p-4">
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div onclick={handleClick}>
      <h2 class="font-medium text-sm leading-snug mb-1" style="color: var(--color-foreground);">
        {product.nombre}
      </h2>
      <p class="text-sm font-medium" style="color: var(--color-muted-foreground);">
        {formatPrice(product.precio)}
      </p>
    </div>

    {#if auth.isAdmin}
      <div class="mt-3 flex gap-3 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
        <button
          onclick={(e) => { e.stopPropagation(); onEdit?.(product); }}
          class="text-xs transition-colors cursor-pointer"
          style="color: var(--color-apple-blue);"
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
