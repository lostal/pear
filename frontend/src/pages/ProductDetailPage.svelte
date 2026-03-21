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
    if (!auth.isAuthenticated) { push('/'); return; }
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

  const GRADIENTS = [
    'linear-gradient(135deg, #e8f4fd 0%, #bee3f8 100%)',
    'linear-gradient(135deg, #f0e8fd 0%, #e9d8fd 100%)',
    'linear-gradient(135deg, #e8fdf0 0%, #c6f6d5 100%)',
    'linear-gradient(135deg, #fdf3e8 0%, #fde8c8 100%)',
    'linear-gradient(135deg, #fde8f4 0%, #fed7e2 100%)',
    'linear-gradient(135deg, #fdfbe8 0%, #fef9c3 100%)',
  ];

  const gradient = $derived(
    product ? GRADIENTS[product.nombre.charCodeAt(0) % 6] : GRADIENTS[0]
  );
</script>

<PageLayout>
  <!-- Back -->
  <button
    onclick={() => push('/products')}
    class="text-sm mb-10 flex items-center gap-1.5 transition-colors cursor-pointer"
    style="color: var(--color-apple-blue);"
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
    <!-- 2-column hero layout -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
      <!-- Left: info -->
      <div>
        <h1
          class="text-4xl sm:text-5xl font-semibold leading-tight mb-6"
          style="letter-spacing: -0.04em;"
        >
          {product.nombre}
        </h1>

        <div class="mb-8">
          <p class="text-xs uppercase tracking-widest mb-2" style="color: var(--color-muted-foreground);">Precio</p>
          <p class="text-4xl font-semibold tabular-nums" style="color: var(--color-apple-blue); letter-spacing: -0.02em;">
            {formatPrice(product.precio)}
          </p>
        </div>

        <button
          onclick={() => push('/products')}
          class="btn-apple"
        >
          Ver más productos
        </button>
      </div>

      <!-- Right: image or gradient placeholder -->
      <div
        class="rounded-3xl aspect-square flex items-center justify-center text-8xl"
        style="background: {gradient};"
      >
        {#if product.imagen}
          <img
            src="/api/uploads/{product.imagen}"
            alt={product.nombre}
            class="w-full h-full object-cover rounded-3xl"
          />
        {:else}
          🍐
        {/if}
      </div>
    </div>
  {/if}
</PageLayout>
