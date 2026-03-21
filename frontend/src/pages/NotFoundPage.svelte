<script lang="ts">
  import { push } from 'svelte-spa-router';
</script>

<div class="min-h-[60vh] flex flex-col items-center justify-center text-center px-4">
  <p
    class="font-black select-none mb-4"
    style="font-size: clamp(5rem, 20vw, 10rem); line-height: 1; color: var(--color-border);"
  >
    404
  </p>
  <h1 class="text-xl font-black mb-2">Página no encontrada</h1>
  <p class="text-sm mb-8" style="color: var(--color-muted-foreground);">
    Esta ruta no existe en el jardín Pear.
  </p>
  <button
    onclick={() => push('/products')}
    class="text-sm font-medium underline underline-offset-4 transition-opacity hover:opacity-70 cursor-pointer"
  >
    Volver al inicio
  </button>
</div>
