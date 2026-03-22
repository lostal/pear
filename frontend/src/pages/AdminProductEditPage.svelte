<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import { toast } from '../stores/toast.svelte.js';
  import {
    fetchProduct, fetchCategories, updateProduct,
    addGrupo, deleteGrupo,
    addOpcionColor, addOpcionStorage, deleteOpcion,
    uploadImagenesOpcion, deleteImagenOpcion,
    uploadImagenesDefault, deleteImagenDefault,
    reorderImagenesDefault, reorderImagenesOpcion,
    reorderOpciones,
  } from '../services/products.service.js';
  import type { Product, Categoria } from '../types/index.js';
  import { getImageUrl } from '../types/index.js';
  import Spinner from '../components/ui/Spinner.svelte';
  import Button from '../components/ui/Button.svelte';
  import PageLayout from '../components/layout/PageLayout.svelte';

  interface Props { params?: { id?: string }; }
  let { params = {} }: Props = $props();

  $effect(() => { if (!auth.isAdmin) push('/'); });

  let product = $state<Product | null>(null);
  let categories = $state<Categoria[]>([]);
  let loading = $state(true);
  let saving = $state(false);

  // ── Campos edición básica
  let nombre = $state('');
  let descripcion = $state('');
  let categoriaId = $state('');
  let precioBase = $state('');
  let activo = $state(true);
  let orden = $state(0);

  // ── Nuevo grupo
  let newGrupoTipo = $state('color');
  let newGrupoNombre = $state('');
  let addingGrupo = $state(false);

  // ── Nueva opción color
  let newColorValor = $state('');
  let newColorHex = $state('#000000');
  let newColorFiles: FileList | null = $state(null);
  let addingColor: Record<string, boolean> = $state({});

  // ── Nueva opción storage
  let newStorageValor = $state('');
  let newStorageModificador = $state('0');
  let addingStorage: Record<string, boolean> = $state({});

  // ── Subida extra de imágenes
  let extraFiles: Record<string, FileList | null> = $state({});
  let uploadingExtra: Record<string, boolean> = $state({});

  // ── Imágenes default
  let defaultFiles: FileList | null = $state(null);
  let uploadingDefault = $state(false);

  // ── Drag & drop imágenes default
  let draggingDefaultIdx = $state<number | null>(null);
  let dragOverDefaultIdx = $state<number | null>(null);

  // ── Drag & drop imágenes por opción (key = oId)
  let draggingOpcionIdx: Record<string, number | null> = $state({});
  let dragOverOpcionIdx: Record<string, number | null> = $state({});

  $effect(() => {
    if (params.id) loadAll(params.id);
  });

  async function loadAll(id: string) {
    loading = true;
    try {
      [product, categories] = await Promise.all([fetchProduct(id), fetchCategories()]);
      if (product) {
        nombre = product.nombre;
        descripcion = product.descripcion ?? '';
        categoriaId = (product.categoria as any)?._id ?? '';
        precioBase = String(product.precioBase);
        activo = product.activo;
        orden = product.orden;
      }
    } catch {
      toast.error('Error al cargar producto');
    } finally {
      loading = false;
    }
  }

  async function handleSaveMeta() {
    if (!product) return;
    saving = true;
    try {
      const updated = await updateProduct(product._id, {
        nombre, descripcion, categoria: categoriaId,
        precioBase: Number(precioBase), activo, orden
      });
      product = updated;
      toast.success('Guardado');
    } catch {
      toast.error('Error al guardar');
    } finally {
      saving = false;
    }
  }

  async function handleAddGrupo() {
    if (!product || !newGrupoNombre) return;
    addingGrupo = true;
    try {
      product = await addGrupo(product._id, { tipo: newGrupoTipo, nombre: newGrupoNombre });
      newGrupoNombre = '';
      toast.success('Grupo añadido');
    } catch {
      toast.error('Error');
    } finally {
      addingGrupo = false;
    }
  }

  async function handleDeleteGrupo(gId: string) {
    if (!product) return;
    try {
      await deleteGrupo(product._id, gId);
      product = await fetchProduct(product._id);
      toast.success('Grupo eliminado');
    } catch {
      toast.error('Error al eliminar grupo');
    }
  }

  async function handleAddColor(gId: string) {
    if (!product || !newColorValor) return;
    addingColor[gId] = true;
    try {
      product = await addOpcionColor(product._id, gId,
        { valor: newColorValor, codigoHex: newColorHex },
        newColorFiles ?? undefined
      );
      newColorValor = ''; newColorHex = '#000000'; newColorFiles = null;
      toast.success('Color añadido');
    } catch {
      toast.error('Error');
    } finally {
      addingColor[gId] = false;
    }
  }

  async function handleAddStorage(gId: string) {
    if (!product || !newStorageValor) return;
    addingStorage[gId] = true;
    try {
      product = await addOpcionStorage(product._id, gId, {
        valor: newStorageValor,
        modificadorPrecio: Number(newStorageModificador)
      });
      newStorageValor = ''; newStorageModificador = '0';
      toast.success('Opción añadida');
    } catch {
      toast.error('Error');
    } finally {
      addingStorage[gId] = false;
    }
  }

  async function handleDeleteOpcion(gId: string, oId: string) {
    if (!product) return;
    try {
      await deleteOpcion(product._id, gId, oId);
      product = await fetchProduct(product._id);
      toast.success('Opción eliminada');
    } catch {
      toast.error('Error');
    }
  }

  async function handleUploadExtra(gId: string, oId: string) {
    if (!product || !extraFiles[oId]?.length) return;
    uploadingExtra[oId] = true;
    try {
      product = await uploadImagenesOpcion(product._id, gId, oId, extraFiles[oId]!);
      extraFiles[oId] = null;
      toast.success('Fotos subidas');
    } catch {
      toast.error('Error al subir');
    } finally {
      uploadingExtra[oId] = false;
    }
  }

  async function handleDeleteImagen(gId: string, oId: string, filename: string) {
    if (!product) return;
    try {
      await deleteImagenOpcion(product._id, gId, oId, filename);
      product = await fetchProduct(product._id);
    } catch {
      toast.error('Error al eliminar');
    }
  }

  async function handleUploadDefault() {
    if (!product || !defaultFiles?.length) return;
    uploadingDefault = true;
    try {
      product = await uploadImagenesDefault(product._id, defaultFiles);
      defaultFiles = null;
      toast.success('Fotos subidas');
    } catch {
      toast.error('Error al subir');
    } finally {
      uploadingDefault = false;
    }
  }

  async function handleDeleteDefault(filename: string) {
    if (!product) return;
    try {
      await deleteImagenDefault(product._id, filename);
      product = await fetchProduct(product._id);
    } catch {
      toast.error('Error al eliminar');
    }
  }

  // ── Drag & drop: imágenes default ─────────────────────────────
  function onDragStartDefault(e: DragEvent, i: number) {
    draggingDefaultIdx = i;
    if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move';
  }
  function onDragOverDefault(e: DragEvent, i: number) {
    e.preventDefault();
    dragOverDefaultIdx = i;
  }
  async function onDropDefault(e: DragEvent, i: number) {
    e.preventDefault();
    if (!product || draggingDefaultIdx === null || draggingDefaultIdx === i) {
      draggingDefaultIdx = null; dragOverDefaultIdx = null; return;
    }
    const arr = [...product.imagenesDefault];
    const [item] = arr.splice(draggingDefaultIdx, 1);
    arr.splice(i, 0, item);
    product.imagenesDefault = arr;
    draggingDefaultIdx = null; dragOverDefaultIdx = null;
    try {
      await reorderImagenesDefault(product._id, arr);
    } catch {
      toast.error('Error al guardar orden');
      product = await fetchProduct(product._id);
    }
  }
  function onDragEndDefault() { draggingDefaultIdx = null; dragOverDefaultIdx = null; }

  // ── Drag & drop: opciones dentro de un grupo ──────────────────
  let draggingOpcionesGrupoIdx: Record<string, number | null> = $state({});
  let dragOverOpcionesGrupoIdx: Record<string, number | null> = $state({});

  function onDragStartOpcionesGrupo(e: DragEvent, gId: string, i: number) {
    draggingOpcionesGrupoIdx[gId] = i;
    if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move';
  }
  function onDragOverOpcionesGrupo(e: DragEvent, gId: string, i: number) {
    e.preventDefault();
    dragOverOpcionesGrupoIdx[gId] = i;
  }
  async function onDropOpcionesGrupo(e: DragEvent, gId: string, opciones: any[], i: number) {
    e.preventDefault();
    const from = draggingOpcionesGrupoIdx[gId];
    if (!product || from === null || from === undefined || from === i) {
      draggingOpcionesGrupoIdx[gId] = null; dragOverOpcionesGrupoIdx[gId] = null; return;
    }
    const arr = [...opciones];
    const [item] = arr.splice(from, 1);
    arr.splice(i, 0, item);
    const grupo = (product.gruposOpciones as any[]).find((g: any) => g._id === gId);
    if (grupo) grupo.opciones = arr;
    draggingOpcionesGrupoIdx[gId] = null; dragOverOpcionesGrupoIdx[gId] = null;
    try {
      await reorderOpciones(product._id, gId, arr.map((o: any) => o._id));
    } catch {
      toast.error('Error al guardar orden');
      product = await fetchProduct(product._id);
    }
  }
  function onDragEndOpcionesGrupo(gId: string) {
    draggingOpcionesGrupoIdx[gId] = null; dragOverOpcionesGrupoIdx[gId] = null;
  }

  // ── Drag & drop: imágenes de opción ───────────────────────────
  function onDragStartOpcion(e: DragEvent, oId: string, i: number) {
    draggingOpcionIdx[oId] = i;
    if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move';
  }
  function onDragOverOpcion(e: DragEvent, oId: string, i: number) {
    e.preventDefault();
    dragOverOpcionIdx[oId] = i;
  }
  async function onDropOpcion(e: DragEvent, gId: string, oId: string, imagenes: string[], i: number) {
    e.preventDefault();
    const from = draggingOpcionIdx[oId];
    if (!product || from === null || from === undefined || from === i) {
      draggingOpcionIdx[oId] = null; dragOverOpcionIdx[oId] = null; return;
    }
    const arr = [...imagenes];
    const [item] = arr.splice(from, 1);
    arr.splice(i, 0, item);
    // update local state
    const grupo = (product.gruposOpciones as any[]).find((g: any) => g._id === gId);
    const opcion = grupo?.opciones.find((o: any) => o._id === oId);
    if (opcion) opcion.imagenes = arr;
    draggingOpcionIdx[oId] = null; dragOverOpcionIdx[oId] = null;
    try {
      await reorderImagenesOpcion(product._id, gId, oId, arr);
    } catch {
      toast.error('Error al guardar orden');
      product = await fetchProduct(product._id);
    }
  }
  function onDragEndOpcion(oId: string) { draggingOpcionIdx[oId] = null; dragOverOpcionIdx[oId] = null; }

  const hasColorGroup = $derived(
    product?.gruposOpciones.some(g => g.tipo === 'color') ?? false
  );
</script>

<style>
  .field label {
    display: block;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--color-muted-foreground);
    margin-bottom: 0.375rem;
  }
  .inp {
    width: 100%;
    padding: 0.625rem 0.875rem;
    font-size: 0.9rem;
    border-radius: 0.625rem;
    border: 1px solid var(--color-border);
    background: var(--color-background);
    color: var(--color-foreground);
    outline: none;
    transition: border-color 0.15s;
  }
  .inp:focus { border-color: var(--color-foreground); }
  .card {
    border: 1px solid var(--color-border);
    border-radius: 1rem;
    padding: 1.5rem;
  }
  .section-title {
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin-bottom: 1.25rem;
    color: var(--color-foreground);
  }
  .section-hint {
    font-size: 0.8rem;
    color: var(--color-muted-foreground);
    margin-top: -0.75rem;
    margin-bottom: 1.25rem;
  }
  .tipo-btn {
    flex: 1;
    padding: 0.875rem 0.5rem;
    border-radius: 0.75rem;
    border: 1.5px solid var(--color-border);
    background: var(--color-background);
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.375rem;
    transition: border-color 0.15s, background 0.15s;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--color-muted-foreground);
  }
  .tipo-btn.selected {
    border-color: var(--color-foreground);
    background: var(--color-secondary);
    color: var(--color-foreground);
  }
  .tipo-btn .icon { font-size: 1.25rem; }

  /* Upload zone */
  .upload-zone {
    border: 1.5px dashed var(--color-border);
    border-radius: 0.75rem;
    padding: 1.25rem;
    text-align: center;
    cursor: pointer;
    position: relative;
    transition: border-color 0.15s, background 0.15s;
  }
  .upload-zone:hover {
    border-color: var(--color-foreground);
    background: var(--color-secondary);
  }
  .upload-zone input[type="file"] {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
    width: 100%;
  }

  /* Grupos */
  .grupo-card {
    border: 1px solid var(--color-border);
    border-radius: 0.875rem;
    overflow: hidden;
  }
  .grupo-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.875rem 1rem;
    background: var(--color-secondary);
    border-bottom: 1px solid var(--color-border);
  }
  .add-option-area {
    padding: 1rem;
    background: var(--color-background);
    border-top: 1px solid var(--color-border);
  }

  /* Imagen grid con drag-and-drop */
  .img-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
    gap: 0.625rem;
    margin-bottom: 1rem;
  }
  .img-item {
    position: relative;
    aspect-ratio: 1;
    border-radius: 0.75rem;
    overflow: hidden;
    cursor: grab;
    border: 2px solid transparent;
    transition: transform 0.1s, border-color 0.15s, opacity 0.15s;
    user-select: none;
  }
  .img-item:active { cursor: grabbing; }
  .img-item.is-dragging { opacity: 0.35; }
  .img-item.is-over {
    border-color: var(--color-foreground);
    transform: scale(1.04);
  }
  .img-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    pointer-events: none;
  }
  .img-portada {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    text-align: center;
    padding: 0.2rem 0;
    background: rgba(0, 0, 0, 0.55);
    color: #fff;
    backdrop-filter: blur(2px);
  }
  .img-num {
    position: absolute;
    top: 0.3rem;
    left: 0.3rem;
    font-size: 0.6rem;
    font-weight: 700;
    background: rgba(0,0,0,0.4);
    color: #fff;
    width: 1.1rem;
    height: 1.1rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .img-delete {
    position: absolute;
    top: 0.3rem;
    right: 0.3rem;
    width: 1.4rem;
    height: 1.4rem;
    border-radius: 50%;
    background: rgba(0,0,0,0.55);
    color: #fff;
    font-size: 0.65rem;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.15s;
    cursor: pointer;
    border: none;
    backdrop-filter: blur(2px);
  }
  .img-item:hover .img-delete { opacity: 1; }

  .drag-hint {
    font-size: 0.72rem;
    color: var(--color-muted-foreground);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
  }

  /* Drag & drop opciones (colores / storage) */
  .opcion-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.75rem;
    border-radius: 0.75rem;
    background: var(--color-secondary);
    border: 2px solid var(--color-border);
    cursor: grab;
    transition: border-color 0.15s, transform 0.1s, opacity 0.15s;
    user-select: none;
  }
  .opcion-item:active { cursor: grabbing; }
  .opcion-item.is-dragging { opacity: 0.35; }
  .opcion-item.is-over {
    border-color: var(--color-foreground);
    transform: scale(1.015);
  }
  .opcion-item.is-cover {
    border-color: var(--color-foreground);
  }
  .cover-badge {
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.1rem 0.45rem;
    border-radius: 0.25rem;
    background: var(--color-foreground);
    color: var(--color-background);
    line-height: 1.5;
  }
  .drag-handle {
    font-size: 0.85rem;
    opacity: 0.35;
    cursor: grab;
    line-height: 1;
  }
</style>

<PageLayout>
  <!-- Breadcrumb + título -->
  <div class="flex items-center gap-3 mb-8">
    <button
      onclick={() => push('/admin/products')}
      class="text-sm cursor-pointer transition-opacity hover:opacity-60 shrink-0"
      style="color: var(--color-muted-foreground);"
    >
      ← Productos
    </button>
    <span style="color: var(--color-border);">/</span>
    <h1 class="text-xl font-bold truncate" style="color: var(--color-foreground);">
      {product?.nombre ?? 'Cargando…'}
    </h1>
    {#if product && !product.activo}
      <span class="text-xs px-2 py-0.5 rounded-full shrink-0"
        style="background: var(--color-secondary); color: var(--color-muted-foreground); border: 1px solid var(--color-border);">
        Inactivo
      </span>
    {/if}
  </div>

  {#if loading}
    <div class="flex justify-center py-24"><Spinner size="lg" /></div>
  {:else if product}
    <div class="flex flex-col gap-8" style="max-width: 680px;">

      <!-- ══ 1. INFORMACIÓN DEL PRODUCTO ══════════════════════════ -->
      <div class="card">
        <p class="section-title">Información del producto</p>

        <div class="flex flex-col gap-5">
          <div class="field">
            <label for="f-nombre">Nombre</label>
            <input id="f-nombre" type="text" placeholder="ej: iPear Pro" bind:value={nombre} class="inp" />
          </div>

          <div class="field">
            <label for="f-desc">Descripción</label>
            <textarea id="f-desc" placeholder="Texto que verá el cliente en la página del producto"
              bind:value={descripcion} rows="3"
              class="inp" style="resize: vertical;"></textarea>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="field">
              <label for="f-cat">Categoría</label>
              <select id="f-cat" bind:value={categoriaId} class="inp">
                <option value="">Sin categoría</option>
                {#each categories as cat}
                  <option value={cat._id}>{cat.nombre}</option>
                {/each}
              </select>
            </div>
            <div class="field">
              <label for="f-precio">Precio base (€)</label>
              <input id="f-precio" type="number" min="0" step="0.01" placeholder="999"
                bind:value={precioBase} class="inp" />
            </div>
          </div>

          <label class="flex items-center gap-3 cursor-pointer select-none" style="color: var(--color-foreground);">
            <span class="relative inline-flex">
              <input type="checkbox" bind:checked={activo} class="sr-only peer" />
              <span class="w-10 h-6 rounded-full border-2 transition-colors peer-checked:border-foreground"
                style="background: var(--color-secondary); border-color: var(--color-border);"
              ></span>
              <span class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full transition-all peer-checked:translate-x-4"
                style="background: var(--color-muted-foreground);"
              ></span>
            </span>
            <span class="text-sm font-medium">Visible en la tienda</span>
          </label>

          <div class="pt-1">
            <Button onclick={handleSaveMeta} loading={saving}>Guardar cambios</Button>
          </div>
        </div>
      </div>

      <!-- ══ 2. FOTOS DEL PRODUCTO (sin grupo de color) ════════════ -->
      {#if !hasColorGroup}
        <div class="card">
          <p class="section-title">Fotos del producto</p>
          <p class="section-hint">La primera foto es la portada. Arrastra para reordenar.</p>

          {#if product.imagenesDefault.length > 0}
            <p class="drag-hint">↕ Arrastra las fotos para cambiar el orden</p>
            <div class="img-grid">
              {#each product.imagenesDefault as img, i (img)}
                <div
                  class="img-item {draggingDefaultIdx === i ? 'is-dragging' : ''} {dragOverDefaultIdx === i && draggingDefaultIdx !== i ? 'is-over' : ''}"
                  draggable="true"
                  ondragstart={(e) => onDragStartDefault(e, i)}
                  ondragover={(e) => onDragOverDefault(e, i)}
                  ondrop={(e) => onDropDefault(e, i)}
                  ondragend={onDragEndDefault}
                  role="listitem"
                >
                  <img src={getImageUrl(img)} alt="Foto {i + 1}" />
                  <span class="img-num">{i + 1}</span>
                  {#if i === 0}
                    <span class="img-portada">Portada</span>
                  {/if}
                  <button
                    class="img-delete"
                    onclick={() => handleDeleteDefault(img)}
                    aria-label="Eliminar foto"
                  >✕</button>
                </div>
              {/each}
            </div>
          {/if}

          <div class="upload-zone">
            <input type="file" multiple accept="image/*"
              onchange={(e) => defaultFiles = (e.target as HTMLInputElement).files}
              id="default-upload" />
            <label for="default-upload" class="pointer-events-none flex flex-col items-center gap-1 py-2">
              <span class="text-2xl">📷</span>
              <p class="text-sm font-medium" style="color: var(--color-foreground);">
                {#if defaultFiles?.length}
                  {defaultFiles.length} foto{defaultFiles.length > 1 ? 's' : ''} lista{defaultFiles.length > 1 ? 's' : ''}
                {:else}
                  Haz clic o arrastra fotos aquí
                {/if}
              </p>
              <p class="text-xs" style="color: var(--color-muted-foreground);">JPG, PNG, WEBP</p>
            </label>
          </div>

          {#if defaultFiles?.length}
            <div class="mt-3">
              <Button onclick={handleUploadDefault} loading={uploadingDefault}>
                Subir {defaultFiles.length} foto{defaultFiles.length > 1 ? 's' : ''}
              </Button>
            </div>
          {/if}
        </div>
      {/if}

      <!-- ══ 3. OPCIONES DE COMPRA ══════════════════════════════════ -->
      <div class="card">
        <p class="section-title">Opciones de compra</p>
        <p class="section-hint">Define los colores, almacenamiento u otras variantes que puede elegir el cliente.</p>

        <!-- Grupos existentes -->
        {#each product.gruposOpciones as grupo (grupo._id)}
          <div class="grupo-card mb-4">
            <div class="grupo-header">
              <div class="flex items-center gap-2">
                <span class="text-base">
                  {grupo.tipo === 'color' ? '🎨' : grupo.tipo === 'storage' ? '💾' : '⚙️'}
                </span>
                <div>
                  <p class="text-sm font-semibold" style="color: var(--color-foreground);">{grupo.nombre}</p>
                  <p class="text-xs capitalize" style="color: var(--color-muted-foreground);">
                    {grupo.tipo === 'color' ? 'Variante de color' : grupo.tipo === 'storage' ? 'Almacenamiento' : 'Opción genérica'}
                    · {grupo.opciones.length} {grupo.opciones.length === 1 ? 'opción' : 'opciones'}
                  </p>
                </div>
              </div>
              <button
                onclick={() => handleDeleteGrupo(grupo._id)}
                class="text-xs cursor-pointer px-2 py-1 rounded-md transition-colors hover:opacity-80"
                style="color: var(--color-destructive); border: 1px solid currentColor;"
              >
                Eliminar grupo
              </button>
            </div>

            <!-- Opciones del grupo -->
            <div class="p-3 flex flex-col gap-2">
              {#if grupo.tipo === 'color' && grupo.opciones.length > 1}
                <p class="drag-hint">↕ Arrastra los colores para cambiar el orden · El primero es la portada de la tienda</p>
              {/if}

              {#each grupo.opciones as opcion, opcionIdx (opcion._id)}
                {@const isColorCover = grupo.tipo === 'color' && opcionIdx === 0 && product.gruposOpciones.findIndex(g => g.tipo === 'color') === product.gruposOpciones.indexOf(grupo)}
                <div
                  class="opcion-item {grupo.tipo === 'color' ? (draggingOpcionesGrupoIdx[grupo._id] === opcionIdx ? 'is-dragging' : '') : ''} {grupo.tipo === 'color' && dragOverOpcionesGrupoIdx[grupo._id] === opcionIdx && draggingOpcionesGrupoIdx[grupo._id] !== opcionIdx ? 'is-over' : ''} {isColorCover ? 'is-cover' : ''}"
                  draggable={grupo.tipo === 'color'}
                  ondragstart={grupo.tipo === 'color' ? (e) => onDragStartOpcionesGrupo(e, grupo._id, opcionIdx) : undefined}
                  ondragover={grupo.tipo === 'color' ? (e) => onDragOverOpcionesGrupo(e, grupo._id, opcionIdx) : undefined}
                  ondrop={grupo.tipo === 'color' ? (e) => onDropOpcionesGrupo(e, grupo._id, grupo.opciones, opcionIdx) : undefined}
                  ondragend={grupo.tipo === 'color' ? () => onDragEndOpcionesGrupo(grupo._id) : undefined}
                  role="listitem"
                  style={grupo.tipo !== 'color' ? 'cursor: default;' : ''}
                >
                  <!-- Cabecera de la opción -->
                  <div class="flex items-center justify-between gap-2">
                    <div class="flex items-center gap-2 flex-1 min-w-0">
                      {#if grupo.tipo === 'color'}
                        <span class="drag-handle">⠿</span>
                      {/if}
                      {#if grupo.tipo === 'color' && (opcion as any).codigoHex}
                        <span class="w-5 h-5 rounded-full border border-black/15 shrink-0"
                          style="background:{(opcion as any).codigoHex};"></span>
                      {/if}
                      <span class="text-sm font-medium truncate">{opcion.valor}</span>
                      {#if isColorCover}
                        <span class="cover-badge shrink-0">Portada</span>
                      {/if}
                      {#if opcion.modificadorPrecio && opcion.modificadorPrecio !== 0}
                        <span class="text-xs shrink-0 px-1.5 py-0.5 rounded"
                          style="background: var(--color-card); color: var(--color-muted-foreground); border: 1px solid var(--color-border);">
                          +{opcion.modificadorPrecio}€
                        </span>
                      {/if}
                    </div>
                    <button onclick={() => handleDeleteOpcion(grupo._id, opcion._id)}
                      class="text-sm leading-none cursor-pointer opacity-40 hover:opacity-100 transition-opacity shrink-0"
                      style="color: var(--color-destructive);"
                      aria-label="Eliminar opción">
                      ✕
                    </button>
                  </div>

                  <!-- Imágenes del color con drag-and-drop -->
                  {#if grupo.tipo === 'color'}
                    {#if (opcion as any).imagenes?.length > 0}
                      <p class="drag-hint" style="margin-bottom: 0.3rem;">↕ Arrastra para reordenar fotos · La primera es la portada del color</p>
                      <div class="img-grid" style="grid-template-columns: repeat(auto-fill, minmax(72px, 1fr));">
                        {#each (opcion as any).imagenes as img, i (img)}
                          <div
                            class="img-item {draggingOpcionIdx[opcion._id] === i ? 'is-dragging' : ''} {dragOverOpcionIdx[opcion._id] === i && draggingOpcionIdx[opcion._id] !== i ? 'is-over' : ''}"
                            draggable="true"
                            ondragstart={(e) => onDragStartOpcion(e, opcion._id, i)}
                            ondragover={(e) => onDragOverOpcion(e, opcion._id, i)}
                            ondrop={(e) => onDropOpcion(e, grupo._id, opcion._id, (opcion as any).imagenes, i)}
                            ondragend={() => onDragEndOpcion(opcion._id)}
                            role="listitem"
                          >
                            <img src={getImageUrl(img)} alt="{opcion.valor} foto {i + 1}" />
                            <span class="img-num">{i + 1}</span>
                            {#if i === 0}
                              <span class="img-portada">Portada</span>
                            {/if}
                            <button
                              class="img-delete"
                              onclick={() => handleDeleteImagen(grupo._id, opcion._id, img)}
                              aria-label="Eliminar foto"
                            >✕</button>
                          </div>
                        {/each}
                      </div>
                    {/if}

                    <!-- Upload fotos extra -->
                    <div class="upload-zone" style="padding: 0.625rem;">
                      <input
                        type="file" multiple accept="image/*"
                        id="extra-{opcion._id}"
                        onchange={(e) => { extraFiles[opcion._id] = (e.target as HTMLInputElement).files; }} />
                      <label for="extra-{opcion._id}" class="text-xs pointer-events-none block" style="color: var(--color-muted-foreground);">
                        {#if extraFiles[opcion._id]?.length}
                          {extraFiles[opcion._id]!.length} foto{extraFiles[opcion._id]!.length > 1 ? 's' : ''} seleccionada{extraFiles[opcion._id]!.length > 1 ? 's' : ''}
                        {:else}
                          + Añadir fotos a este color
                        {/if}
                      </label>
                    </div>
                    {#if extraFiles[opcion._id]?.length}
                      <Button onclick={() => handleUploadExtra(grupo._id, opcion._id)} loading={uploadingExtra[opcion._id] ?? false}>
                        Subir {extraFiles[opcion._id]!.length} foto{extraFiles[opcion._id]!.length > 1 ? 's' : ''}
                      </Button>
                    {/if}
                  {/if}
                </div>
              {/each}

              {#if grupo.opciones.length === 0}
                <p class="text-xs text-center py-3" style="color: var(--color-muted-foreground);">
                  Sin opciones aún. Añade una abajo.
                </p>
              {/if}
            </div>

            <!-- Formulario añadir opción -->
            <div class="add-option-area">
              {#if grupo.tipo === 'color'}
                <p class="text-xs font-semibold uppercase tracking-wide mb-3"
                  style="color: var(--color-muted-foreground);">Nuevo color</p>
                <div class="flex flex-col gap-3">
                  <div class="field">
                    <label for="color-nombre-{grupo._id}">Nombre del color</label>
                    <input id="color-nombre-{grupo._id}" type="text" placeholder="ej: Negro Sideral"
                      bind:value={newColorValor} class="inp" />
                  </div>
                  <div class="field">
                    <label for="color-hex-{grupo._id}">Color</label>
                    <div class="flex items-center gap-3">
                      <div class="relative" style="width: 3rem; height: 3rem;">
                        <div class="w-12 h-12 rounded-lg border overflow-hidden"
                          style="border-color: var(--color-border); background: {newColorHex};">
                        </div>
                        <input id="color-hex-{grupo._id}" type="color" bind:value={newColorHex}
                          class="absolute inset-0 opacity-0 w-full h-full cursor-pointer" />
                      </div>
                      <span class="text-sm font-mono" style="color: var(--color-muted-foreground);">{newColorHex}</span>
                    </div>
                  </div>
                  <div class="field">
                    <label for="color-fotos-{grupo._id}">Fotos (opcional)</label>
                    <div class="upload-zone">
                      <input id="color-fotos-{grupo._id}" type="file" multiple accept="image/*"
                        onchange={(e) => newColorFiles = (e.target as HTMLInputElement).files} />
                      <p class="text-sm pointer-events-none" style="color: var(--color-muted-foreground);">
                        {#if newColorFiles?.length}
                          {newColorFiles.length} foto{newColorFiles.length > 1 ? 's' : ''} seleccionada{newColorFiles.length > 1 ? 's' : ''}
                        {:else}
                          Haz clic para seleccionar fotos
                        {/if}
                      </p>
                    </div>
                  </div>
                  <Button onclick={() => handleAddColor(grupo._id)}
                    loading={addingColor[grupo._id] ?? false}
                    disabled={!newColorValor}>
                    Añadir color
                  </Button>
                </div>
              {:else}
                <p class="text-xs font-semibold uppercase tracking-wide mb-3"
                  style="color: var(--color-muted-foreground);">Nueva opción</p>
                <div class="flex flex-col gap-3">
                  <div class="grid grid-cols-2 gap-3">
                    <div class="field">
                      <label for="storage-valor-{grupo._id}">Valor</label>
                      <input id="storage-valor-{grupo._id}" type="text" placeholder="ej: 256 GB"
                        bind:value={newStorageValor} class="inp" />
                    </div>
                    <div class="field">
                      <label for="storage-precio-{grupo._id}">Precio extra (€)</label>
                      <input id="storage-precio-{grupo._id}" type="number" placeholder="0" min="0"
                        bind:value={newStorageModificador} class="inp" />
                    </div>
                  </div>
                  <Button onclick={() => handleAddStorage(grupo._id)}
                    loading={addingStorage[grupo._id] ?? false}
                    disabled={!newStorageValor}>
                    Añadir opción
                  </Button>
                </div>
              {/if}
            </div>
          </div>
        {/each}

        <!-- Añadir nuevo grupo -->
        <div class="mt-2 pt-5 border-t" style="border-color: var(--color-border);">
          <p class="text-sm font-semibold mb-4" style="color: var(--color-foreground);">Añadir grupo de opciones</p>

          <div class="flex gap-3 mb-4">
            <button class="tipo-btn {newGrupoTipo === 'color' ? 'selected' : ''}"
              onclick={() => newGrupoTipo = 'color'}>
              <span class="icon">🎨</span>
              Color
            </button>
            <button class="tipo-btn {newGrupoTipo === 'storage' ? 'selected' : ''}"
              onclick={() => newGrupoTipo = 'storage'}>
              <span class="icon">💾</span>
              Almacenamiento
            </button>
            <button class="tipo-btn {newGrupoTipo === 'button' ? 'selected' : ''}"
              onclick={() => newGrupoTipo = 'button'}>
              <span class="icon">⚙️</span>
              Genérico
            </button>
          </div>

          <div class="field mb-4">
            <label for="grupo-nombre">Etiqueta del grupo</label>
            <input id="grupo-nombre" type="text"
              placeholder={newGrupoTipo === 'color' ? 'ej: Color' : newGrupoTipo === 'storage' ? 'ej: Almacenamiento' : 'ej: Conectividad'}
              bind:value={newGrupoNombre} class="inp" />
          </div>
          <Button onclick={handleAddGrupo} loading={addingGrupo} disabled={!newGrupoNombre}>
            Crear grupo
          </Button>
        </div>
      </div>

    </div>
  {/if}
</PageLayout>
