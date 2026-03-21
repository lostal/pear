<script lang="ts">
  import type { Product } from '../../types/index.js';
  import Modal from '../ui/Modal.svelte';

  interface Props {
    open: boolean;
    product: Product | null;
    onclose: () => void;
  }

  let { open, product, onclose }: Props = $props();

  function formatPrice(price: number) {
    return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(price);
  }
</script>

<Modal {open} title={product?.nombre ?? ''} {onclose}>
  {#if product}
    <div class="flex flex-col gap-4">
      <div class="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p class="text-[var(--color-muted-foreground)] mb-1">Precio</p>
          <p class="font-bold text-xl">{formatPrice(product.precio)}</p>
        </div>
        <div>
          <p class="text-[var(--color-muted-foreground)] mb-1">ID</p>
          <p class="font-mono text-xs break-all">{product._id}</p>
        </div>
      </div>

      {#if product.imagen}
        <img src="/api/uploads/{product.imagen}" alt={product.nombre} class="rounded-md max-h-48 object-contain" />
      {/if}
    </div>
  {/if}
</Modal>
