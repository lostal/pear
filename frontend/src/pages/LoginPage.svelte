<script lang="ts">
  import { push } from '../lib/router.svelte.js';
  import { withTransition } from '../lib/transitions.js';
  import { onMount } from 'svelte';
  import { animate } from 'motion';
  import { auth } from '../stores/auth.svelte.js';
  import { login } from '../services/auth.service.js';
  import { toast } from '../stores/toast.svelte.js';
  import Button from '../components/ui/Button.svelte';
  import Input from '../components/ui/Input.svelte';

  let username = $state('');
  let password = $state('');
  let loading = $state(false);
  let error = $state('');
  let card: HTMLElement | undefined = $state();

  $effect(() => {
    if (auth.isAuthenticated) push('/products');
  });

  onMount(() => {
    if (card) {
      animate(
        card,
        { opacity: [0, 1], y: [24, 0] },
        { duration: 0.45, easing: [0.25, 0.1, 0.25, 1] }
      );
    }
  });

  async function handleSubmit(e: SubmitEvent) {
    e.preventDefault();
    error = '';
    loading = true;
    try {
      await login({ username, password });
      toast.success(`Bienvenido, ${auth.displayName}.`);
      withTransition(() => push('/products'));
    } catch (err) {
      error = err instanceof Error ? err.message : 'Error al iniciar sesión.';
    } finally {
      loading = false;
    }
  }
</script>

<div
  class="min-h-[calc(100vh-64px)] flex flex-col items-center justify-center px-4 py-12"
  style="background-color: var(--color-background);"
>
  <!-- Logo -->
  <div class="mb-8 text-center">
    <p class="text-4xl font-black tracking-tight">Pear</p>
    <p class="text-sm mt-2" style="color: var(--color-muted-foreground);">
      Inicia sesión para continuar
    </p>
  </div>

  <!-- Card -->
  <div
    bind:this={card}
    class="w-full max-w-sm rounded-lg border p-8"
    style="opacity:0; background: var(--color-card); border-color: var(--color-border);"
  >
    <form onsubmit={handleSubmit} class="flex flex-col gap-5">
      <Input
        bind:value={username}
        label="Usuario"
        placeholder="tu_usuario"
        required
        disabled={loading}
      />
      <Input
        bind:value={password}
        type="password"
        label="Contraseña"
        placeholder="••••••••"
        required
        disabled={loading}
      />

      {#if error}
        <p
          class="text-xs px-3 py-2 rounded-md border"
          style="color: var(--color-destructive); border-color: var(--color-destructive); background: color-mix(in srgb, var(--color-destructive) 8%, transparent);"
        >
          {error}
        </p>
      {/if}

      <Button type="submit" {loading} disabled={loading} class="w-full mt-1">Iniciar sesión</Button>
    </form>
  </div>

  <p class="text-xs mt-8" style="color: var(--color-muted-foreground); opacity: 0.4;">
    Pear · PW2 2025–26
  </p>
</div>
