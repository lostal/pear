<script lang="ts">
  import { push, router } from 'svelte-spa-router';
  import { auth } from '../../stores/auth.svelte.js';
  import { theme } from '../../lib/theme.svelte.js';
  import { withTransition } from '../../lib/transitions.js';

  function navigate(path: string) {
    withTransition(() => push(path));
  }

  function handleLogout() {
    auth.logout();
    withTransition(() => push('/login'));
  }

  function toggleTheme() {
    theme.set(theme.current === 'dark' ? 'light' : 'dark');
  }

  const navLinks = $derived([
    { path: '/products', label: 'Productos' },
    { path: '/profile', label: 'Perfil' },
    ...(auth.isAdmin ? [{ path: '/admin/users', label: 'Usuarios' }] : []),
  ]);

  function isActive(path: string): boolean {
    const loc = router.location;
    if (path === '/products' && (loc === '/' || loc.startsWith('/products'))) return true;
    return loc.startsWith(path);
  }
</script>

<nav class="sticky top-0 z-40 border-b border-[var(--color-border)] bg-[var(--color-background)]/95 backdrop-blur-sm">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 flex h-14 items-center gap-6">
    <!-- Logo -->
    <button
      onclick={() => navigate('/products')}
      class="flex items-center gap-1.5 font-black text-lg tracking-tight hover:opacity-70 transition-opacity cursor-pointer"
    >
      <span class="text-[var(--color-pear)]">i</span>Pear
    </button>

    <!-- Nav links -->
    <div class="flex items-center gap-1 flex-1">
      {#each navLinks as link}
        {@const active = isActive(link.path)}
        <button
          onclick={() => navigate(link.path)}
          class="px-3 py-1 text-sm rounded-md transition-colors cursor-pointer relative
            {active
              ? 'text-[var(--color-foreground)] font-semibold'
              : 'text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)]'}"
        >
          {link.label}
          {#if active}
            <span class="absolute bottom-0 left-0 right-0 h-0.5 bg-[var(--color-pear)] rounded-full"></span>
          {/if}
        </button>
      {/each}
    </div>

    <!-- Right side -->
    <div class="flex items-center gap-3">
      <span class="text-sm text-[var(--color-muted-foreground)] hidden sm:block">
        {auth.displayName}
        {#if auth.isAdmin}
          <span class="ml-1 text-xs text-[var(--color-pear)] font-medium">(admin)</span>
        {/if}
      </span>

      <!-- Theme toggle -->
      <button
        onclick={toggleTheme}
        class="p-1.5 rounded-md hover:bg-[var(--color-accent)] transition-colors text-[var(--color-muted-foreground)] cursor-pointer"
        aria-label="Cambiar tema"
      >
        {#if theme.current === 'dark'}
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5" /><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
          </svg>
        {:else}
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
          </svg>
        {/if}
      </button>

      <button
        onclick={handleLogout}
        class="text-sm text-[var(--color-muted-foreground)] hover:text-[var(--color-destructive)] transition-colors cursor-pointer"
      >
        Salir
      </button>
    </div>
  </div>
</nav>
