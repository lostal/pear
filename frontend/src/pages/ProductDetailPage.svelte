<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import { toast } from '../stores/toast.svelte.js';
  import { fetchProduct } from '../services/products.service.js';
  import type { Product } from '../types/index.js';
  import Spinner from '../components/ui/Spinner.svelte';
  import Button from '../components/ui/Button.svelte';

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

<div class="max-w-2xl mx-auto px-4 sm:px-6 py-8">
  <Button variant="ghost" size="sm" onclick={() => push('/products')} class="mb-6">
    ← Volver
  </Button>

  {#if loading}
    <div class="flex justify-center py-20"><Spinner size="lg" /></div>
  {:else if error}
    <div class="text-center py-16">
      <p class="text-[var(--color-destructive)]">{error}</p>
    </div>
  {:else if product}
    <div class="bg-[var(--color-card)] border border-[var(--color-border)] rounded-lg p-8">
      <h1 class="text-3xl font-black tracking-tight mb-6">{product.nombre}</h1>

      {#if product.imagen}
        <img src="/api/uploads/{product.imagen}" alt={product.nombre} class="rounded-md max-h-64 object-contain mb-6" />
      {/if}

      <div class="py-6 border-t border-[var(--color-border)]">
        <p class="text-sm text-[var(--color-muted-foreground)] mb-1">Precio</p>
        <p class="text-4xl font-black">{formatPrice(product.precio)}</p>
      </div>
    </div>
  {/if}
</div>
