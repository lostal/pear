<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import { theme } from '../lib/theme.svelte.js';
  import Button from '../components/ui/Button.svelte';
  import Badge from '../components/ui/Badge.svelte';

  $effect(() => {
    if (!auth.isAuthenticated) push('/login');
  });

  function handleLogout() {
    auth.logout();
    push('/login');
  }

  type ThemeVal = 'light' | 'dark' | 'system';
  const themeOptions: { value: ThemeVal; label: string }[] = [
    { value: 'light', label: 'Claro' },
    { value: 'dark', label: 'Oscuro' },
    { value: 'system', label: 'Sistema' },
  ];
</script>

<div class="max-w-2xl mx-auto px-4 sm:px-6 py-8">
  <h1 class="text-2xl font-black tracking-tight mb-6">Perfil</h1>

  {#if auth.user}
    <div class="bg-[var(--color-card)] border border-[var(--color-border)] rounded-lg p-6 mb-4">
      <div class="flex items-center gap-4 mb-4">
        <div class="h-14 w-14 rounded-full bg-[var(--color-pear-muted)] flex items-center justify-center text-2xl font-black text-[var(--color-pear)]">
          {auth.user.username[0].toUpperCase()}
        </div>
        <div>
          <p class="font-bold text-xl">{auth.user.username}</p>
        </div>
        <Badge variant={auth.isAdmin ? 'success' : 'muted'} class="ml-auto">
          {auth.user.role}
        </Badge>
      </div>
    </div>

    <div class="bg-[var(--color-card)] border border-[var(--color-border)] rounded-lg p-6 mb-4">
      <h2 class="font-semibold mb-4">Apariencia</h2>
      <div class="flex gap-2">
        {#each themeOptions as opt}
          <button
            onclick={() => theme.set(opt.value)}
            class="flex-1 py-2 text-sm rounded-md border transition-colors cursor-pointer
              {theme.current === opt.value
                ? 'border-[var(--color-pear)] bg-[var(--color-pear-muted)] text-[var(--color-pear)] font-semibold'
                : 'border-[var(--color-border)] hover:bg-[var(--color-accent)]'}"
          >
            {opt.label}
          </button>
        {/each}
      </div>
    </div>

    <Button variant="destructive" onclick={handleLogout} class="w-full">
      Cerrar sesión
    </Button>
  {/if}
</div>
