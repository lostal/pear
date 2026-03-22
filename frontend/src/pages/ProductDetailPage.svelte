<script lang="ts">
  import { push } from '../lib/router.svelte.js';
  import { withTransition } from '../lib/transitions.js';
  import { auth } from '../stores/auth.svelte.js';
  import { toast } from '../stores/toast.svelte.js';
  import { fetchProduct } from '../services/products.service.js';
  import { products as productsStore } from '../stores/products.svelte.js';
  import { http } from '../services/http.js';
  import type { Product, OpcionColor, Opcion } from '../types/index.js';
  import { getImagenesForProduct, getPrecioTotal } from '../types/index.js';
  import { formatPrice } from '../lib/utils.js';
  import ProductImageGallery from '../components/products/ProductImageGallery.svelte';
  import ColorSwatch from '../components/products/ColorSwatch.svelte';
  import StorageSelector from '../components/products/StorageSelector.svelte';
  import Spinner from '../components/ui/Spinner.svelte';
  import PageLayout from '../components/layout/PageLayout.svelte';
  import { ChevronLeft } from 'lucide-svelte';

  interface Props {
    params?: { id?: string };
  }

  let { params = {} }: Props = $props();

  const cached = productsStore.list.find((p) => p._id === params?.id) ?? null;
  let product = $state<Product | null>(cached);
  let loading = $state(!cached);
  let addingToCart = $state(false);

  let selectedColor = $state<OpcionColor | null>(null);
  let selectedStorage = $state<Opcion | null>(null);

  const colorGrupo = $derived(product?.gruposOpciones.find((g) => g.tipo === 'color'));
  const storageGrupos = $derived(
    product?.gruposOpciones.filter((g) => g.tipo === 'storage' || g.tipo === 'button') ?? []
  );

  const imagenes = $derived(product ? getImagenesForProduct(product, selectedColor?.valor) : []);
  const precio = $derived(product ? getPrecioTotal(product, selectedStorage?.valor) : 0);

  $effect(() => {
    if (params.id) loadProduct(params.id);
  });

  // Auto-seleccionar primera opción de cada grupo
  $effect(() => {
    if (colorGrupo?.opciones.length && !selectedColor) {
      selectedColor = colorGrupo.opciones[0] as OpcionColor;
    }
  });

  async function loadProduct(id: string) {
    if (!product) loading = true;
    try {
      product = await fetchProduct(id);
    } catch {
      toast.error('Error al cargar el producto.');
    } finally {
      loading = false;
    }
  }

  async function addToCart() {
    if (!product || !auth.isAuthenticated) {
      push('/login');
      return;
    }
    addingToCart = true;
    try {
      await http.post('/api/cart/add', {
        productId: product._id,
        colorValor: selectedColor?.valor,
        storageValor: selectedStorage?.valor,
      });
      toast.success('Añadido al carrito');
    } catch {
      toast.error('Error al añadir al carrito');
    } finally {
      addingToCart = false;
    }
  }
</script>

<PageLayout>
  <button
    onclick={() => withTransition(() => push('/products'))}
    class="text-sm mb-10 flex items-center gap-1 transition-opacity hover:opacity-70 cursor-pointer group"
    style="color: var(--color-muted-foreground);"
  >
    <ChevronLeft size={16} class="transition-transform group-hover:-translate-x-0.5" />
    Tienda
  </button>

  {#if loading}
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-start">
      <!-- Placeholder imagen con view-transition-name para que la tarjeta vuele aquí -->
      <div
        class="aspect-square rounded-2xl"
        style="background: var(--color-secondary); view-transition-name: {params.id
          ? `product-image-${params.id}`
          : ''};"
      ></div>
      <!-- Placeholder título -->
      <div class="flex flex-col gap-6">
        <div
          class="h-14 rounded-xl"
          style="background: var(--color-secondary); view-transition-name: {params.id
            ? `product-title-${params.id}`
            : ''};"
        ></div>
        <Spinner size="lg" />
      </div>
    </div>
  {:else if product}
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-start">
      <!-- Galería -->
      <div
        class="lg:sticky lg:top-24"
        style="view-transition-name: {params.id ? `product-image-${params.id}` : ''};"
      >
        <ProductImageGallery {imagenes} alt={product.nombre} />
      </div>

      <!-- Configurador -->
      <div class="flex flex-col gap-6">
        <!-- Nombre y categoría -->
        {#if product.categoria}
          <p
            class="text-xs uppercase tracking-widest font-medium"
            style="color: var(--color-muted-foreground);"
          >
            {product.categoria.nombre}
          </p>
        {/if}
        <h1
          class="text-4xl sm:text-5xl font-black leading-tight"
          style="view-transition-name: {params.id ? `product-title-${params.id}` : ''};"
        >
          {product.nombre}
        </h1>

        <!-- Precio -->
        <p class="text-3xl font-bold tabular-nums">
          {formatPrice(precio)}
        </p>

        <!-- Descripción -->
        {#if product.descripcion}
          <p class="text-sm leading-relaxed" style="color: var(--color-muted-foreground);">
            {product.descripcion}
          </p>
        {/if}

        <div class="h-px" style="background: var(--color-border);"></div>

        <!-- Color -->
        {#if colorGrupo && colorGrupo.opciones.length > 0}
          <div>
            <p class="text-sm font-medium mb-3">
              Color — <span style="color: var(--color-muted-foreground);"
                >{selectedColor?.valor ?? ''}</span
              >
            </p>
            <ColorSwatch
              opciones={colorGrupo.opciones as OpcionColor[]}
              selected={selectedColor?.valor}
              onselect={(op) => {
                selectedColor = op;
              }}
            />
          </div>
        {/if}

        <!-- Storage / opciones extra -->
        {#each storageGrupos as grupo}
          <div>
            <p class="text-sm font-medium mb-3">{grupo.nombre}</p>
            <StorageSelector
              {grupo}
              selected={selectedStorage?.valor}
              precioBase={product.precioBase}
              onselect={(op) => {
                selectedStorage = op;
              }}
            />
          </div>
        {/each}

        <!-- Botón carrito -->
        <button
          onclick={addToCart}
          disabled={addingToCart}
          class="w-full py-4 rounded-2xl font-semibold text-base transition-opacity cursor-pointer disabled:opacity-50"
          style="background: var(--color-foreground); color: var(--color-background);"
        >
          {#if addingToCart}
            Añadiendo...
          {:else if auth.isAuthenticated}
            Añadir al carrito
          {:else}
            Inicia sesión para comprar
          {/if}
        </button>
      </div>
    </div>
  {/if}
</PageLayout>
