<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import { toast } from '../stores/toast.svelte.js';
  import {
    fetchProducts, fetchCategories,
    createCategory, deleteCategory,
    createProduct, deleteProduct
  } from '../services/products.service.js';
  import type { Product, Categoria } from '../types/index.js';
  import Spinner from '../components/ui/Spinner.svelte';
  import Button from '../components/ui/Button.svelte';
  import PageLayout from '../components/layout/PageLayout.svelte';

  $effect(() => {
    if (!auth.isAuthenticated || !auth.isAdmin) push('/');
  });

  let productList = $state<Product[]>([]);
  let categoryList = $state<Categoria[]>([]);
  let loading = $state(true);
  let tab = $state<'products' | 'categories'>('products');

  // ── Form: nueva categoría
  let catNombre = $state('');
  let catLoading = $state(false);

  // Slug se genera automáticamente desde el nombre
  const catSlug = $derived(
    catNombre.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
  );

  // ── Form: nuevo producto
  let prodNombre = $state('');
  let prodCategoria = $state('');
  let prodPrecio = $state('');
  let prodLoading = $state(false);

  $effect(() => {
    loadAll();
  });

  async function loadAll() {
    loading = true;
    try {
      [productList, categoryList] = await Promise.all([fetchProducts(), fetchCategories()]);
    } catch {
      toast.error('Error al cargar datos');
    } finally {
      loading = false;
    }
  }

  async function handleCreateCategory() {
    if (!catNombre.trim() || !catSlug) return;
    catLoading = true;
    try {
      const cat = await createCategory({
        nombre: catNombre.trim(),
        slug: catSlug,
        orden: categoryList.length
      });
      categoryList = [...categoryList, cat];
      catNombre = '';
      toast.success('Categoría creada');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Error');
    } finally {
      catLoading = false;
    }
  }

  async function handleDeleteCategory(id: string) {
    try {
      await deleteCategory(id);
      categoryList = categoryList.filter(c => c._id !== id);
      toast.success('Categoría eliminada');
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'No se puede eliminar: tiene productos asociados');
    }
  }

  async function handleCreateProduct() {
    if (!prodNombre.trim() || !prodCategoria || !prodPrecio) return;
    prodLoading = true;
    try {
      const p = await createProduct({
        nombre: prodNombre.trim(),
        categoria: prodCategoria,
        precioBase: Number(prodPrecio)
      });
      productList = [...productList, p];
      prodNombre = ''; prodCategoria = ''; prodPrecio = '';
      toast.success('Producto creado');
      push(`/admin/products/${p._id}`);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Error');
    } finally {
      prodLoading = false;
    }
  }

  async function handleDeleteProduct(id: string) {
    try {
      await deleteProduct(id);
      productList = productList.filter(p => p._id !== id);
      toast.success('Producto desactivado');
    } catch {
      toast.error('Error al eliminar');
    }
  }

  const inputStyle = 'border-color: var(--color-border); background: var(--color-card); color: var(--color-foreground);';
  const inputClass = 'w-full px-3 py-2 text-sm rounded-lg border outline-none focus:ring-1';
</script>

<PageLayout>
  <div class="flex items-center justify-between mb-8 gap-4">
    <h1 class="text-3xl font-black">Panel de productos</h1>
    <button
      onclick={() => push('/products')}
      class="text-sm transition-opacity hover:opacity-70 cursor-pointer"
      style="color: var(--color-muted-foreground);"
    >
      ← Volver a la tienda
    </button>
  </div>

  <!-- Tabs -->
  <div class="flex gap-6 mb-8 border-b" style="border-color: var(--color-border);">
    {#each [['products', 'Productos'], ['categories', 'Categorías']] as [key, label]}
      <button
        onclick={() => tab = key as any}
        class="pb-3 text-sm font-medium border-b-2 -mb-px transition-colors cursor-pointer"
        style={tab === key
          ? 'border-color: var(--color-foreground); color: var(--color-foreground);'
          : 'border-color: transparent; color: var(--color-muted-foreground);'}
      >
        {label}
      </button>
    {/each}
  </div>

  {#if loading}
    <div class="flex justify-center py-16"><Spinner size="lg" /></div>

  {:else if tab === 'categories'}
    <!-- ─── Categorías ──────────────────────────────────────────── -->
    <div class="max-w-lg flex flex-col gap-8">

      <!-- Crear categoría -->
      <div class="flex flex-col gap-3">
        <h2 class="text-base font-semibold">Nueva categoría</h2>
        <input
          type="text"
          placeholder="Nombre (ej: iPear, AirPears…)"
          bind:value={catNombre}
          class={inputClass}
          style={inputStyle}
        />
        {#if catNombre}
          <p class="text-xs -mt-1" style="color: var(--color-muted-foreground);">
            Slug: <span class="font-mono">{catSlug}</span>
          </p>
        {/if}
        <Button
          onclick={handleCreateCategory}
          loading={catLoading}
          disabled={!catNombre.trim()}
        >
          Crear categoría
        </Button>
      </div>

      <!-- Lista de categorías -->
      {#if categoryList.length > 0}
        <div class="flex flex-col gap-2">
          <h2 class="text-base font-semibold">Categorías existentes</h2>
          {#each categoryList.sort((a, b) => a.orden - b.orden) as cat (cat._id)}
            <div
              class="flex items-center justify-between px-4 py-3 rounded-xl border"
              style="border-color: var(--color-border); background: var(--color-card);"
            >
              <div>
                <p class="text-sm font-medium">{cat.nombre}</p>
                <p class="text-xs font-mono" style="color: var(--color-muted-foreground);">/{cat.slug}</p>
              </div>
              <button
                onclick={() => handleDeleteCategory(cat._id)}
                class="text-xs cursor-pointer hover:opacity-70 transition-opacity"
                style="color: var(--color-destructive);"
              >
                Eliminar
              </button>
            </div>
          {/each}
        </div>
      {:else}
        <p class="text-sm" style="color: var(--color-muted-foreground);">
          Crea al menos una categoría antes de añadir productos.
        </p>
      {/if}
    </div>

  {:else}
    <!-- ─── Productos ───────────────────────────────────────────── -->
    <div class="flex flex-col gap-8">

      <!-- Crear producto -->
      <div class="max-w-lg flex flex-col gap-3">
        <h2 class="text-base font-semibold">Nuevo producto</h2>

        {#if categoryList.length === 0}
          <p class="text-sm p-4 rounded-xl border" style="border-color: var(--color-border); color: var(--color-muted-foreground);">
            Primero crea una categoría en la pestaña "Categorías".
          </p>
        {:else}
          <input
            type="text"
            placeholder="Nombre (ej: iPear Pro)"
            bind:value={prodNombre}
            class={inputClass}
            style={inputStyle}
          />
          <select
            bind:value={prodCategoria}
            class={inputClass}
            style={inputStyle}
          >
            <option value="">Selecciona categoría</option>
            {#each categoryList as cat}
              <option value={cat._id}>{cat.nombre}</option>
            {/each}
          </select>
          <input
            type="number"
            placeholder="Precio base en €"
            bind:value={prodPrecio}
            class={inputClass}
            style={inputStyle}
          />
          <Button
            onclick={handleCreateProduct}
            loading={prodLoading}
            disabled={!prodNombre.trim() || !prodCategoria || !prodPrecio}
          >
            Crear y configurar variantes →
          </Button>
        {/if}
      </div>

      <!-- Lista de productos -->
      {#if productList.length > 0}
        <div class="flex flex-col gap-2">
          <h2 class="text-base font-semibold">Todos los productos</h2>
          {#each productList as p (p._id)}
            <div
              class="flex items-center justify-between px-4 py-3 rounded-xl border"
              style="border-color: var(--color-border); background: var(--color-card);"
            >
              <div>
                <p class="text-sm font-medium">
                  {p.nombre}
                  {#if !p.activo}
                    <span class="text-xs opacity-40 ml-1">(inactivo)</span>
                  {/if}
                </p>
                <p class="text-xs" style="color: var(--color-muted-foreground);">
                  {p.categoria?.nombre ?? '—'} · desde {p.precioBase}€
                </p>
              </div>
              <div class="flex gap-4 text-xs shrink-0">
                <button
                  onclick={() => push(`/admin/products/${p._id}`)}
                  class="cursor-pointer hover:opacity-70 transition-opacity"
                  style="color: var(--color-foreground);"
                >
                  Editar
                </button>
                <button
                  onclick={() => handleDeleteProduct(p._id)}
                  class="cursor-pointer hover:opacity-70 transition-opacity"
                  style="color: var(--color-destructive);"
                >
                  Desactivar
                </button>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</PageLayout>
