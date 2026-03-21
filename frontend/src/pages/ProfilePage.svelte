<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import { theme } from '../lib/theme.svelte.js';
  import Button from '../components/ui/Button.svelte';
  import PageLayout from '../components/layout/PageLayout.svelte';

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

<PageLayout>
  {#if auth.user}
    <!-- Sección: info de usuario -->
    <div class="pb-8 mb-8 border-b border-[var(--color-border)] flex items-center gap-5">
      <div class="h-16 w-16 rounded-full bg-[var(--color-pear-muted)] flex items-center justify-center text-2xl font-black text-[var(--color-pear)]">
        {auth.user.username[0].toUpperCase()}
      </div>
      <div>
        <h2 class="text-2xl font-black tracking-tight">{auth.user.username}</h2>
        <p class="text-xs font-bold uppercase tracking-widest text-[var(--color-muted-foreground)] mt-0.5">
          {auth.user.role}
        </p>
      </div>
    </div>

    <!-- Sección: apariencia -->
    <div class="pb-8 mb-8 border-b border-[var(--color-border)]">
      <h3 class="text-xs font-bold uppercase tracking-widest text-[var(--color-muted-foreground)] mb-4">Apariencia</h3>
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

    <!-- Acción: cerrar sesión -->
    <Button variant="destructive" onclick={handleLogout} class="w-full sm:w-auto">
      Cerrar sesión
    </Button>
  {/if}
</PageLayout>
