<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import { products } from '../stores/products.svelte.js';
  import { toast } from '../stores/toast.svelte.js';
  import {
    fetchProducts,
    createProduct,
    updateProduct,
    deleteProduct,
  } from '../services/products.service.js';
  import type { Product } from '../types/index.js';
  import ProductGrid from '../components/products/ProductGrid.svelte';
  import ProductFilters from '../components/products/ProductFilters.svelte';
  import ProductForm from '../components/products/ProductForm.svelte';
  import ProductModal from '../components/products/ProductModal.svelte';
  import ConfirmDialog from '../components/ui/ConfirmDialog.svelte';
  import Modal from '../components/ui/Modal.svelte';
  import Button from '../components/ui/Button.svelte';

  $effect(() => {
    if (!auth.isAuthenticated) push('/login');
  });

  $effect(() => {
    if (auth.isAuthenticated) loadProducts();
  });

  async function loadProducts() {
    products.setLoading(true);
    try {
      const list = await fetchProducts();
      products.setList(list);
    } catch {
      toast.error('Error al cargar los productos.');
    } finally {
      products.setLoading(false);
    }
  }

  let viewProduct = $state<Product | null>(null);
  let showView = $state(false);
  let editProduct = $state<Product | null>(null);
  let showForm = $state(false);
  let deleteTarget = $state<Product | null>(null);
  let showConfirm = $state(false);
  let deleting = $state(false);

  function openCreate() { editProduct = null; showForm = true; }
  function openEdit(p: Product) { editProduct = p; showForm = true; }
  function openDelete(p: Product) { deleteTarget = p; showConfirm = true; }
  function openView(p: Product) { viewProduct = p; showView = true; }

  async function handleSave(data: { nombre: string; precio: number }) {
    try {
      if (editProduct) {
        const updated = await updateProduct(editProduct._id, data);
        products.updateProduct(updated);
        toast.success('Producto actualizado.');
      } else {
        const created = await createProduct(data);
        products.addProduct(created);
        toast.success('Producto creado.');
      }
      showForm = false;
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Error al guardar.');
      throw err;
    }
  }

  async function handleDelete() {
    if (!deleteTarget) return;
    deleting = true;
    try {
      await deleteProduct(deleteTarget._id);
      products.removeProduct(deleteTarget._id);
      toast.success('Producto eliminado.');
      showConfirm = false;
    } catch {
      toast.error('Error al eliminar el producto.');
    } finally {
      deleting = false;
    }
  }
</script>

<div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
  <div class="flex items-center justify-between mb-6">
    <div>
      <h1 class="text-2xl font-black tracking-tight">Productos</h1>
      <p class="text-sm text-[var(--color-muted-foreground)] mt-0.5">Catálogo iPear</p>
    </div>
    {#if auth.isAdmin}
      <Button onclick={openCreate}>
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        Nuevo producto
      </Button>
    {/if}
  </div>

  <div class="mb-6">
    <ProductFilters />
  </div>

  <ProductGrid
    products={products.filtered}
    loading={products.loading}
    onEdit={openEdit}
    onDelete={openDelete}
    onView={openView}
  />
</div>

<ProductModal open={showView} product={viewProduct} onclose={() => (showView = false)} />

<Modal
  open={showForm}
  title={editProduct ? 'Editar producto' : 'Nuevo producto'}
  onclose={() => (showForm = false)}
>
  <ProductForm
    product={editProduct}
    onSave={handleSave}
    onCancel={() => (showForm = false)}
  />
</Modal>

<ConfirmDialog
  open={showConfirm}
  title="¿Eliminar producto?"
  message="Se eliminará «{deleteTarget?.nombre}» permanentemente."
  confirmLabel="Eliminar"
  loading={deleting}
  onconfirm={handleDelete}
  oncancel={() => (showConfirm = false)}
/>
