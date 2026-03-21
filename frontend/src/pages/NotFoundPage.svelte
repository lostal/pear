<script lang="ts">
  import { push } from 'svelte-spa-router';
  import Button from '../components/ui/Button.svelte';
</script>

<div class="min-h-[60vh] flex flex-col items-center justify-center text-center px-4">
  <p class="text-7xl mb-4">🍐</p>
  <h1 class="text-4xl font-black tracking-tight mb-2">404</h1>
  <p class="text-[var(--color-muted-foreground)] mb-8">Esta página no existe en el jardín iPear.</p>
  <Button onclick={() => push('/products')}>Volver al inicio</Button>
</div>
