<script lang="ts">
  import { onMount } from 'svelte';
  import { push } from '../lib/router.svelte.js';
  import { withTransition } from '../lib/transitions.js';
  import { auth } from '../stores/auth.svelte.js';
  import { products } from '../stores/products.svelte.js';
  import { toast } from '../stores/toast.svelte.js';
  import { fetchProducts } from '../services/products.service.js';
  import CategorySection from '../components/products/CategorySection.svelte';
  import Spinner from '../components/ui/Spinner.svelte';
  import Button from '../components/ui/Button.svelte';
  import PageLayout from '../components/layout/PageLayout.svelte';

  onMount(() => {
    loadProducts();
  });

  async function loadProducts() {
    if (products.list.length === 0) products.setLoading(true);
    try {
      const list = await fetchProducts();
      products.setList(list);
    } catch {
      toast.error('Error al cargar los productos.');
    } finally {
      products.setLoading(false);
    }
  }
</script>

<PageLayout>
  <!-- Header -->
  <div class="flex items-end justify-between gap-4 mb-12">
    <div>
      <h1 class="text-4xl sm:text-5xl font-black">Tienda</h1>
      <p class="text-sm mt-1.5" style="color: var(--color-muted-foreground);">Catálogo Pear</p>
    </div>
    {#if auth.isAdmin}
      <Button onclick={() => withTransition(() => push('/admin/products'))}>Panel admin</Button>
    {/if}
  </div>

  {#if products.loading}
    <div class="flex justify-center py-24"><Spinner size="lg" /></div>
  {:else if products.byCategory.length === 0}
    <div class="text-center py-24">
      <p class="text-lg" style="color: var(--color-muted-foreground);">
        No hay productos disponibles.
      </p>
    </div>
  {:else}
    {#each products.byCategory as group (group.categoria._id ?? group.categoria.slug)}
      <CategorySection {group} />
    {/each}
  {/if}
</PageLayout>
