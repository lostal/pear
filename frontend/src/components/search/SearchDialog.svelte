<script lang="ts">
  import { onMount } from 'svelte';
  import { flushSync } from 'svelte';
  import { fade } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  import { push } from '../../lib/router.svelte.js';
  import { uiState } from '../../lib/ui.svelte.js';
  import { fetchProducts } from '../../services/products.service.js';
  import type { Product } from '../../types/index.js';
  import { getImagenesForProduct, getImageUrl } from '../../types/index.js';

  function dialogFly(
    node: Element,
    { duration = 250, y = -24 }: { duration?: number; y?: number } = {}
  ) {
    return {
      duration,
      easing: cubicOut,
      css: (t: number) => {
        const offset = (1 - t) * y;
        const s = 0.97 + 0.03 * t;
        return `transform: translateY(${offset}px) scale(${s}); opacity: ${t}`;
      },
    };
  }

  let products = $state<Product[]>([]);
  let query = $state('');
  let loaded = $state(false);
  // When true the {#if} goes false instantly (no Svelte out-transition) so
  // startViewTransition captures a clean new state without the dialog in it.
  let navigating = $state(false);

  let filteredProducts = $derived(
    query.length > 0
      ? products.filter((p) => p.nombre.toLowerCase().includes(query.toLowerCase()))
      : []
  );

  let searchInput = $state<HTMLInputElement>();

  $effect(() => {
    if (uiState.isSearchOpen) {
      navigating = false;
      setTimeout(() => searchInput?.focus(), 10);
      if (!loaded) {
        fetchProducts()
          .then((data) => {
            products = data;
            loaded = true;
          })
          .catch(() => {});
      }
    }
  });

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') uiState.closeSearch();
  }

  function goToProduct(id: string) {
    // navigating=true is queued but NOT yet flushed to DOM.
    // startViewTransition captures OLD state while dialog is still visible.
    // flushSync inside the callback flushes navigating=true → {#if} goes false
    // instantly, dialog removed with no Svelte out-transition → clean new state.
    navigating = true;

    if (!('startViewTransition' in document)) {
      uiState.isSearchOpen = false;
      navigating = false;
      push('/products/' + id);
      return;
    }

    document.startViewTransition(() => {
      flushSync(() => push('/products/' + id));
    }).finished.finally(() => {
      uiState.isSearchOpen = false;
      navigating = false;
    });
  }

  onMount(() => {
    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  });

  const fmt = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' });
</script>

{#if uiState.isSearchOpen && !navigating}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="fixed inset-0 z-[100] flex items-start justify-center pt-8 sm:pt-24 px-4"
    style="background: rgba(0,0,0,0.4); backdrop-filter: blur(4px);"
    transition:fade={{ duration: 180 }}
    onclick={() => uiState.closeSearch()}
  >
    <div
      class="w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col"
      style="background: var(--color-card); border: 1px solid var(--color-border);"
      in:dialogFly={{ duration: 250, y: -24 }}
      out:dialogFly={{ duration: 180, y: -12 }}
      onclick={(e) => e.stopPropagation()}
    >
      <!-- Input -->
      <div
        class="flex items-center gap-3 p-4 sm:p-6 border-b"
        style="border-color: var(--color-border); background: color-mix(in srgb, var(--color-background) 50%, transparent);"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="w-5 h-5"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          style="color: var(--color-muted-foreground);"
        >
          <circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" />
        </svg>
        <input
          bind:this={searchInput}
          bind:value={query}
          type="text"
          placeholder="Buscar productos..."
          class="flex-1 border-none outline-none text-base sm:text-lg font-medium"
          style="background: transparent; color: var(--color-foreground);"
        />
        <button
          onclick={() => uiState.closeSearch()}
          class="sm:hidden text-xs font-bold uppercase tracking-widest cursor-pointer"
          style="color: var(--color-muted-foreground);"
        >
          Cancelar
        </button>
      </div>

      <!-- Results -->
      <div class="max-h-[60vh] sm:max-h-[400px] overflow-y-auto p-2 sm:p-4">
        {#if query.length === 0}
          <div class="p-12 text-center">
            <p class="text-xs font-bold uppercase tracking-[0.2em]" style="color: var(--color-muted-foreground);">
              Escribe para buscar...
            </p>
          </div>
        {:else if filteredProducts.length === 0}
          <div class="p-12 text-center">
            <p class="text-xs font-bold uppercase tracking-[0.2em]" style="color: var(--color-muted-foreground);">
              Sin resultados para "{query}"
            </p>
          </div>
        {:else}
          <div class="space-y-1">
            {#each filteredProducts as product (product._id)}
              {@const img = getImagenesForProduct(product)[0]}
              <button
                class="w-full text-left p-4 sm:p-5 rounded-xl transition-all cursor-pointer flex items-center gap-3"
                style="background: transparent;"
                onmouseenter={(e) => (e.currentTarget as HTMLElement).style.background = 'var(--color-accent)'}
                onmouseleave={(e) => (e.currentTarget as HTMLElement).style.background = 'transparent'}
                onclick={() => goToProduct(product._id)}
              >
                <div class="flex-1 min-w-0">
                  <p class="text-sm sm:text-base font-bold" style="color: var(--color-foreground);">
                    {product.nombre}
                  </p>
                  <p class="text-xs sm:text-sm mt-0.5" style="color: var(--color-muted-foreground);">
                    {fmt.format(product.precioBase)}
                  </p>
                </div>
                <div class="flex-shrink-0 w-12 h-12 rounded-xl overflow-hidden" style="background: #d9d9d9;">
                  {#if img}
                    <img src={getImageUrl(img)} alt={product.nombre} class="w-full h-full object-contain" draggable="false" />
                  {/if}
                </div>
              </button>
            {/each}
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}
