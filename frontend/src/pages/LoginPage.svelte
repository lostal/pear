<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import { login } from '../services/auth.service.js';
  import { toast } from '../stores/toast.svelte.js';
  import Button from '../components/ui/Button.svelte';
  import Input from '../components/ui/Input.svelte';

  let username = $state('');
  let password = $state('');
  let loading = $state(false);
  let error = $state('');

  $effect(() => {
    if (auth.isAuthenticated) push('/products');
  });

  async function handleSubmit(e: SubmitEvent) {
    e.preventDefault();
    error = '';
    loading = true;
    try {
      await login({ username, password });
      toast.success(`Bienvenido, ${auth.displayName}!`);
      push('/products');
    } catch (err) {
      error = err instanceof Error ? err.message : 'Error al iniciar sesión.';
    } finally {
      loading = false;
    }
  }
</script>

<div class="min-h-screen flex flex-col items-center justify-center px-4">
  <!-- Logo grande -->
  <div class="mb-10 text-center">
    <p class="text-6xl sm:text-7xl font-black tracking-tight">
      <span class="font-serif italic text-[var(--color-pear)]">i</span>Pear
    </p>
    <p class="text-xs font-bold uppercase tracking-widest text-[var(--color-muted-foreground)] mt-3">
      Inicia sesión para continuar
    </p>
  </div>

  <!-- Card -->
  <div class="w-full max-w-sm rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)]/50 p-8 shadow-sm">
    <form onsubmit={handleSubmit} class="flex flex-col gap-4">
      <Input
        bind:value={username}
        label="Usuario"
        placeholder="tu_usuario"
        required
        disabled={loading}
        labelClass="text-xs font-bold uppercase tracking-widest"
      />
      <Input
        bind:value={password}
        type="password"
        label="Contraseña"
        placeholder="••••••••"
        required
        disabled={loading}
        labelClass="text-xs font-bold uppercase tracking-widest"
      />

      {#if error}
        <p class="text-sm text-[var(--color-destructive)] bg-red-50 dark:bg-red-900/10 px-3 py-2 rounded-md">
          {error}
        </p>
      {/if}

      <Button type="submit" {loading} disabled={loading} class="w-full mt-2">
        Iniciar sesión
      </Button>
    </form>
  </div>

  <p class="text-xs font-bold uppercase tracking-widest text-[var(--color-muted-foreground)] opacity-50 mt-8">
    iPear · Parodia Conceptual
  </p>
</div>
