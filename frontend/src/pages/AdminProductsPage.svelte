<script lang="ts">
  import { untrack } from 'svelte';
  import { push } from '../lib/router.svelte.js';
  import { withTransition } from '../lib/transitions.js';
  import { auth } from '../stores/auth.svelte.js';
  import { toast } from '../stores/toast.svelte.js';
  import {
    fetchProducts,
    fetchCategories,
    createCategory,
    deleteCategory,
    createProduct,
    deleteProduct,
    reorderCategories,
    reorderProductsBatch,
  } from '../services/products.service.js';
  import type { Product, Categoria } from '../types/index.js';
  import Spinner from '../components/ui/Spinner.svelte';
  import ConfirmDialog from '../components/ui/ConfirmDialog.svelte';
  import Button from '../components/ui/Button.svelte';
  import PageLayout from '../components/layout/PageLayout.svelte';
  import { GripVertical, Pencil, Trash2, ChevronLeft } from 'lucide-svelte';

  $effect(() => {
    if (!auth.isAuthenticated || !auth.isAdmin) push('/');
  });

  type Group = { cat: Categoria; products: Product[] };

  let productList = $state<Product[]>([]);
  let categoryList = $state<Categoria[]>([]);
  let groups = $state<Group[]>([]);
  let loading = $state(true);
  let tab = $state<'products' | 'categories'>('products');

  // ── Form: nueva categoría
  let catNombre = $state('');
  let catLoading = $state(false);
  const catSlug = $derived(
    catNombre
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^a-z0-9-]/g, '')
  );

  // ── Form: nuevo producto
  let prodNombre = $state('');
  let prodCategoria = $state('');
  let prodPrecio = $state('');
  let prodLoading = $state(false);

  // ── Drag: categorías
  let deleteTarget = $state<Product | null>(null);
  let deleting = $state(false);

  // ── Drag: categorías
  let draggingCatIdx = $state<number | null>(null);
  let dragOverCatIdx = $state<number | null>(null);

  // ── Drag: productos dentro de una categoría (keyed por catId)
  let draggingProdIdx: Record<string, number | null> = $state({});
  let dragOverProdIdx: Record<string, number | null> = $state({});

  $effect(() => {
    untrack(() => loadAll());
  });

  function buildGroups() {
    groups = [...categoryList]
      .sort((a, b) => a.orden - b.orden)
      .map((cat) => ({
        cat,
        products: [...productList]
          .filter((p) => p.categoria._id === cat._id)
          .sort((a, b) => a.orden - b.orden),
      }));
  }

  async function loadAll() {
    loading = true;
    try {
      [productList, categoryList] = await Promise.all([fetchProducts(), fetchCategories()]);
      buildGroups();
    } catch {
      toast.error('Error al cargar datos');
    } finally {
      loading = false;
    }
  }

  // ── Categorías ─────────────────────────────────────────────────

  async function handleCreateCategory() {
    if (!catNombre.trim() || !catSlug) return;
    catLoading = true;
    try {
      const cat = await createCategory({
        nombre: catNombre.trim(),
        slug: catSlug,
        orden: categoryList.length,
      });
      categoryList = [...categoryList, cat];
      buildGroups();
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
      categoryList = categoryList.filter((c) => c._id !== id);
      buildGroups();
      toast.success('Categoría eliminada');
    } catch (err) {
      toast.error(
        err instanceof Error ? err.message : 'No se puede eliminar: tiene productos asociados'
      );
    }
  }

  // ── Productos ──────────────────────────────────────────────────

  async function handleCreateProduct() {
    if (!prodNombre.trim() || !prodCategoria || !prodPrecio) return;
    prodLoading = true;
    try {
      const p = await createProduct({
        nombre: prodNombre.trim(),
        categoria: prodCategoria,
        precioBase: Number(prodPrecio),
      });
      productList = [...productList, p];
      prodNombre = '';
      prodCategoria = '';
      prodPrecio = '';
      toast.success('Producto creado');
      withTransition(() => push(`/admin/products/${p._id}`));
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Error');
    } finally {
      prodLoading = false;
    }
  }

  async function handleConfirmDelete() {
    if (!deleteTarget) return;
    const target = deleteTarget;
    deleting = true;
    try {
      await deleteProduct(target._id);
      productList = productList.filter((p) => p._id !== target._id);
      buildGroups();
      toast.success('Producto eliminado');
      deleteTarget = null;
    } catch {
      toast.error('Error al eliminar');
    } finally {
      deleting = false;
    }
  }

  // ── Drag & drop: categorías ────────────────────────────────────

  function onDragStartCat(e: DragEvent, i: number) {
    draggingCatIdx = i;
    if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move';
  }
  function onDragOverCat(e: DragEvent, i: number) {
    e.preventDefault();
    dragOverCatIdx = i;
  }
  async function onDropCat(e: DragEvent, i: number) {
    e.preventDefault();
    const from = draggingCatIdx;
    if (from === null || from === i) {
      draggingCatIdx = null;
      dragOverCatIdx = null;
      return;
    }
    const arr = [...groups];
    const [item] = arr.splice(from, 1);
    arr.splice(i, 0, item);
    groups = arr;
    draggingCatIdx = null;
    dragOverCatIdx = null;
    try {
      await reorderCategories(arr.map((g) => g.cat._id));
    } catch {
      toast.error('Error al guardar orden');
      buildGroups();
    }
  }
  function onDragEndCat() {
    draggingCatIdx = null;
    dragOverCatIdx = null;
  }

  // ── Drag & drop: productos ─────────────────────────────────────

  function onDragStartProd(e: DragEvent, catId: string, i: number) {
    draggingProdIdx[catId] = i;
    if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move';
  }
  function onDragOverProd(e: DragEvent, catId: string, i: number) {
    e.preventDefault();
    dragOverProdIdx[catId] = i;
  }
  async function onDropProd(e: DragEvent, catId: string, i: number) {
    e.preventDefault();
    const from = draggingProdIdx[catId];
    if (from === null || from === undefined || from === i) {
      draggingProdIdx[catId] = null;
      dragOverProdIdx[catId] = null;
      return;
    }
    const gIdx = groups.findIndex((g) => g.cat._id === catId);
    const prods = [...groups[gIdx].products];
    const [item] = prods.splice(from, 1);
    prods.splice(i, 0, item);
    groups[gIdx].products = prods;
    draggingProdIdx[catId] = null;
    dragOverProdIdx[catId] = null;
    try {
      await reorderProductsBatch(prods.map((p) => p._id));
    } catch {
      toast.error('Error al guardar orden');
      buildGroups();
    }
  }
  function onDragEndProd(catId: string) {
    draggingProdIdx[catId] = null;
    dragOverProdIdx[catId] = null;
  }

  const inputStyle =
    'border-color: var(--color-border); background: var(--color-card); color: var(--color-foreground);';
  const inputClass = 'w-full px-3 py-2 text-sm rounded-lg border outline-none focus:ring-1';
</script>

<PageLayout>
  <div class="flex items-center justify-between mb-8 gap-4">
    <h1 class="text-3xl font-black">Panel de productos</h1>
    <button
      onclick={() => withTransition(() => push('/products'))}
      class="text-sm flex items-center gap-1 transition-opacity hover:opacity-70 cursor-pointer group"
      style="color: var(--color-muted-foreground);"
    >
      <ChevronLeft size={16} class="transition-transform group-hover:-translate-x-0.5" />
      Tienda
    </button>
  </div>

  <!-- Tabs -->
  <div class="flex gap-6 mb-8 border-b" style="border-color: var(--color-border);">
    <button
      onclick={() => (tab = 'products')}
      class="pb-3 text-sm font-medium border-b-2 -mb-px transition-colors cursor-pointer"
      style={tab === 'products'
        ? 'border-color: var(--color-foreground); color: var(--color-foreground);'
        : 'border-color: transparent; color: var(--color-muted-foreground);'}>Productos</button
    >
    <button
      onclick={() => (tab = 'categories')}
      class="pb-3 text-sm font-medium border-b-2 -mb-px transition-colors cursor-pointer"
      style={tab === 'categories'
        ? 'border-color: var(--color-foreground); color: var(--color-foreground);'
        : 'border-color: transparent; color: var(--color-muted-foreground);'}>Categorías</button
    >
  </div>

  {#if loading}
    <div class="flex justify-center py-16"><Spinner size="lg" /></div>
  {:else if tab === 'categories'}
    <!-- ─── Categorías ──────────────────────────────────────────── -->
    <div class="max-w-lg flex flex-col gap-8">
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
        <Button onclick={handleCreateCategory} loading={catLoading} disabled={!catNombre.trim()}>
          Crear categoría
        </Button>
      </div>

      {#if categoryList.length > 0}
        <div class="flex flex-col gap-2">
          <h2 class="text-base font-semibold">Categorías existentes</h2>
          {#each [...categoryList].sort((a, b) => a.orden - b.orden) as cat (cat._id)}
            <div
              class="flex items-center justify-between px-4 py-3 rounded-xl border"
              style="border-color: var(--color-border); background: var(--color-card);"
            >
              <div>
                <p class="text-sm font-medium">{cat.nombre}</p>
                <p class="text-xs font-mono" style="color: var(--color-muted-foreground);">
                  /{cat.slug}
                </p>
              </div>
              <button
                onclick={() => handleDeleteCategory(cat._id)}
                class="flex items-center gap-1 text-xs cursor-pointer hover:opacity-70 transition-opacity"
                style="color: var(--color-destructive);"
              >
                <Trash2 size={12} />
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
    <div class="flex flex-col gap-10">
      <!-- Crear producto -->
      <div class="max-w-lg flex flex-col gap-3">
        <h2 class="text-base font-semibold">Nuevo producto</h2>
        {#if categoryList.length === 0}
          <p
            class="text-sm p-4 rounded-xl border"
            style="border-color: var(--color-border); color: var(--color-muted-foreground);"
          >
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
          <select bind:value={prodCategoria} class={inputClass} style={inputStyle}>
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

      <!-- Lista de productos agrupada por categoría -->
      {#if groups.length > 0}
        <div class="flex flex-col gap-3" style="max-width: 720px;">
          <div class="flex items-center justify-between">
            <h2 class="text-base font-semibold">Todos los productos</h2>
            <span class="text-xs" style="color: var(--color-muted-foreground);">
              {productList.length} producto{productList.length !== 1 ? 's' : ''}
              · arrastra para reordenar
            </span>
          </div>

          {#each groups as group, catIdx (group.cat._id)}
            <div
              class="cat-group {draggingCatIdx === catIdx ? 'is-dragging' : ''} {dragOverCatIdx ===
                catIdx && draggingCatIdx !== catIdx
                ? 'is-over'
                : ''}"
              draggable="true"
              ondragstart={(e) => onDragStartCat(e, catIdx)}
              ondragover={(e) => onDragOverCat(e, catIdx)}
              ondrop={(e) => onDropCat(e, catIdx)}
              ondragend={onDragEndCat}
              role="group"
            >
              <!-- Cabecera de categoría -->
              <div class="cat-header">
                <GripVertical size={14} class="drag-handle" />
                <span class="text-sm font-semibold" style="color: var(--color-foreground);"
                  >{group.cat.nombre}</span
                >
                <span class="text-xs" style="color: var(--color-muted-foreground);">
                  {group.products.length} producto{group.products.length !== 1 ? 's' : ''}
                </span>
              </div>

              <!-- Productos de esta categoría -->
              <div class="p-1.5 flex flex-col gap-0.5">
                {#if group.products.length === 0}
                  <p class="text-xs px-3 py-2" style="color: var(--color-muted-foreground);">
                    Sin productos en esta categoría.
                  </p>
                {:else}
                  {#each group.products as prod, prodIdx (prod._id)}
                    <div
                      class="prod-row {draggingProdIdx[group.cat._id] === prodIdx
                        ? 'is-dragging'
                        : ''} {dragOverProdIdx[group.cat._id] === prodIdx &&
                      draggingProdIdx[group.cat._id] !== prodIdx
                        ? 'is-over'
                        : ''}"
                      draggable="true"
                      ondragstart={(e) => onDragStartProd(e, group.cat._id, prodIdx)}
                      ondragover={(e) => onDragOverProd(e, group.cat._id, prodIdx)}
                      ondrop={(e) => onDropProd(e, group.cat._id, prodIdx)}
                      ondragend={() => onDragEndProd(group.cat._id)}
                      role="listitem"
                    >
                      <GripVertical size={14} class="drag-handle" />
                      <div class="flex-1 min-w-0">
                        <p
                          class="text-sm font-medium truncate"
                          style="color: var(--color-foreground);"
                        >
                          {prod.nombre}
                        </p>
                        <p class="text-xs" style="color: var(--color-muted-foreground);">
                          desde {prod.precioBase}€
                          {#if !prod.activo}<span class="opacity-50"> · Inactivo</span>{/if}
                        </p>
                      </div>
                      <div class="flex gap-1 shrink-0">
                        <button
                          onclick={() => push(`/admin/products/${prod._id}`)}
                          class="flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-md cursor-pointer transition-colors hover:opacity-80"
                          style="color: var(--color-foreground); background: var(--color-secondary); border: 1px solid var(--color-border);"
                        >
                          <Pencil size={12} />
                          Editar
                        </button>
                        <button
                          onclick={() => (deleteTarget = prod)}
                          class="flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-md cursor-pointer transition-opacity hover:opacity-70"
                          style="color: var(--color-destructive);"
                        >
                          <Trash2 size={12} />
                        </button>
                      </div>
                    </div>
                  {/each}
                {/if}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</PageLayout>

<ConfirmDialog
  open={!!deleteTarget}
  title="¿Eliminar producto?"
  message="Se eliminará «{deleteTarget?.nombre}» de forma permanente."
  confirmLabel="Eliminar"
  loading={deleting}
  onconfirm={handleConfirmDelete}
  oncancel={() => (deleteTarget = null)}
/>

<style>
  /* Drag: categorías */
  .cat-group {
    border: 1.5px solid var(--color-border);
    border-radius: 0.875rem;
    overflow: hidden;
    transition:
      opacity 0.15s,
      border-color 0.15s;
    user-select: none;
  }
  .cat-group.is-dragging {
    opacity: 0.35;
  }
  .cat-group.is-over {
    border-color: var(--color-foreground);
  }

  .cat-header {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    padding: 0.625rem 0.875rem;
    background: var(--color-secondary);
    cursor: grab;
  }
  .cat-header:active {
    cursor: grabbing;
  }

  /* Drag: productos */
  .prod-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem;
    cursor: grab;
    border: 1.5px solid transparent;
    transition:
      background 0.1s,
      border-color 0.1s,
      opacity 0.15s;
  }
  .prod-row:hover {
    background: var(--color-secondary);
  }
  .prod-row:active {
    cursor: grabbing;
  }
  .prod-row.is-dragging {
    opacity: 0.35;
  }
  .prod-row.is-over {
    border-color: var(--color-foreground);
    background: var(--color-secondary);
  }

  .drag-handle {
    color: var(--color-muted-foreground);
    opacity: 0.35;
    flex-shrink: 0;
  }
  .cat-header:hover :global(.drag-handle),
  .prod-row:hover :global(.drag-handle) {
    opacity: 0.7;
  }
</style>
