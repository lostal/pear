<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import { toast } from '../stores/toast.svelte.js';
  import { fetchProduct } from '../services/products.service.js';
  import type { Product } from '../types/index.js';
  import Spinner from '../components/ui/Spinner.svelte';
  import PageLayout from '../components/layout/PageLayout.svelte';

  interface Props {
    params?: { id?: string };
  }

  let { params = {} }: Props = $props();

  let product = $state<Product | null>(null);
  let loading = $state(true);
  let error = $state('');

  $effect(() => {
    if (params.id) loadProduct(params.id);
  });

  async function loadProduct(id: string) {
    loading = true;
    error = '';
    try {
      product = await fetchProduct(id);
    } catch (err) {
      error = err instanceof Error ? err.message : 'Error al cargar el producto.';
      toast.error(error);
    } finally {
      loading = false;
    }
  }

  function formatPrice(price: number) {
    return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(price);
  }

  const initial = $derived(product ? product.nombre.charAt(0).toUpperCase() : '');
</script>

<PageLayout>
  <!-- Back -->
  <button
    onclick={() => push('/products')}
    class="text-sm mb-10 flex items-center gap-1.5 transition-opacity hover:opacity-70 cursor-pointer"
    style="color: var(--color-muted-foreground);"
  >
    ← Volver a la tienda
  </button>

  {#if loading}
    <div class="flex justify-center py-20"><Spinner size="lg" /></div>
  {:else if error}
    <div class="text-center py-16">
      <p style="color: var(--color-destructive);">{error}</p>
    </div>
  {:else if product}
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
      <!-- Info -->
      <div>
        <h1 class="text-4xl sm:text-5xl font-black leading-tight mb-6">
          {product.nombre}
        </h1>

        <div class="mb-8">
          <p class="text-xs uppercase tracking-widest mb-2" style="color: var(--color-muted-foreground);">Precio</p>
          <p class="text-4xl font-black tabular-nums">
            {formatPrice(product.precio)}
          </p>
        </div>

        <button
          onclick={() => push('/products')}
          class="inline-flex items-center justify-center font-medium text-sm px-5 py-2.5 rounded-md border transition-colors hover:bg-accent cursor-pointer"
          style="border-color: var(--color-border); color: var(--color-foreground);"
        >
          Ver más productos
        </button>
      </div>

      <!-- Imagen o placeholder -->
      <div
        class="rounded-2xl aspect-square flex items-center justify-center overflow-hidden"
        style="background: var(--color-secondary);"
      >
        {#if product.imagen}
          <img
            src="/api/uploads/{product.imagen}"
            alt={product.nombre}
            class="w-full h-full object-cover rounded-2xl"
          />
        {:else}
          <span
            class="font-black select-none"
            style="font-size: clamp(5rem, 15vw, 9rem); line-height: 1; color: var(--color-border);"
          >{initial}</span>
        {/if}
      </div>
    </div>
  {/if}
</PageLayout>
