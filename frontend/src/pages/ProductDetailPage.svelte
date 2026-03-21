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
    if (!auth.isAuthenticated) { push('/login'); return; }
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
</script>

<PageLayout>
  <!-- Volver -->
  <button
    onclick={() => push('/products')}
    class="text-xs font-bold uppercase tracking-widest text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)] mb-12 flex items-center gap-2 transition-colors cursor-pointer"
  >
    ← Volver
  </button>

  {#if loading}
    <div class="flex justify-center py-20"><Spinner size="lg" /></div>
  {:else if error}
    <div class="text-center py-16">
      <p class="text-[var(--color-destructive)]">{error}</p>
    </div>
  {:else if product}
    <!-- Nombre del producto: ENORME -->
    <h1 class="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-tight mb-8">
      {product.nombre}
    </h1>

    {#if product.imagen}
      <img
        src="/api/uploads/{product.imagen}"
        alt={product.nombre}
        class="rounded-2xl w-full max-h-80 object-cover mb-12"
      />
    {/if}

    <!-- Precio: serif gigante -->
    <div class="border-t border-[var(--color-border)] pt-8">
      <p class="text-xs font-bold uppercase tracking-widest text-[var(--color-muted-foreground)] mb-3">Precio</p>
      <p class="font-serif text-5xl sm:text-6xl tabular-nums">{formatPrice(product.precio)}</p>
    </div>
  {/if}
</PageLayout>
