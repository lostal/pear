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

<div class="min-h-screen flex items-center justify-center bg-[var(--color-background)] px-4">
  <div class="w-full max-w-sm">
    <!-- Logo -->
    <div class="text-center mb-8">
      <h1 class="text-4xl font-black tracking-tight">
        <span class="text-[var(--color-pear)]">i</span>Pear
      </h1>
      <p class="text-[var(--color-muted-foreground)] text-sm mt-1">Inicia sesión para continuar</p>
    </div>

    <!-- Card -->
    <div class="bg-[var(--color-card)] border border-[var(--color-border)] rounded-lg p-6 shadow-sm">
      <form onsubmit={handleSubmit} class="flex flex-col gap-4">
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
          <p class="text-sm text-[var(--color-destructive)] bg-red-50 dark:bg-red-900/10 px-3 py-2 rounded-md">
            {error}
          </p>
        {/if}

        <Button type="submit" {loading} disabled={loading} class="w-full mt-1">
          Iniciar sesión
        </Button>
      </form>
    </div>

    <p class="text-center text-xs text-[var(--color-muted-foreground)] mt-6">
      iPear · Parodia Conceptual
    </p>
  </div>
</div>
