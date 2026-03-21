<script lang="ts">
  import { push, router } from 'svelte-spa-router';
  import { auth } from '../../stores/auth.svelte.js';
  import { theme } from '../../lib/theme.svelte.js';
  import { withTransition } from '../../lib/transitions.js';

  let container: HTMLElement | undefined = $state();

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

  $effect(() => {
    function onScroll() {
      container?.classList.toggle('scrolled', window.scrollY > 50);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return () => window.removeEventListener('scroll', onScroll);
  });
</script>

<header
  id="ipear-header"
  bind:this={container}
  class="sticky top-0 z-40 backdrop-blur-md bg-[var(--color-background)]/80 border-b border-[var(--color-border)] transition-all duration-300"
>
  <div class="header-inner max-w-5xl mx-auto px-4 sm:px-6 flex items-center gap-6 py-4 sm:py-5 transition-all duration-300">
    <!-- Logo -->
    <button
      onclick={() => navigate('/products')}
      class="logo-btn flex items-center font-black text-xl sm:text-2xl tracking-normal hover:opacity-70 transition-opacity cursor-pointer"
    >
      <span class="font-serif italic text-[var(--color-pear)]">i</span>Pear
    </button>

    <!-- Nav links -->
    <nav class="flex items-center gap-1 flex-1">
      {#each navLinks as link}
        {@const active = isActive(link.path)}
        <button
          onclick={() => navigate(link.path)}
          class="px-3 py-1.5 text-xs font-bold uppercase tracking-widest rounded-md transition-colors cursor-pointer relative
            {active
              ? 'text-[var(--color-foreground)]'
              : 'text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)] hover:bg-[var(--color-accent)]'}"
        >
          {link.label}
          {#if active}
            <span class="absolute bottom-0 left-2 right-2 h-[2px] bg-[var(--color-pear)] rounded-full"></span>
          {/if}
        </button>
      {/each}
    </nav>

    <!-- Right side -->
    <div class="flex items-center gap-2">
      <span class="text-xs text-[var(--color-muted-foreground)] hidden sm:block">
        {auth.displayName}
        {#if auth.isAdmin}
          <span class="ml-1 text-[var(--color-pear)] font-bold">(admin)</span>
        {/if}
      </span>

      <!-- Theme toggle -->
      <button
        onclick={toggleTheme}
        class="p-2 rounded-md hover:bg-[var(--color-accent)] transition-colors text-[var(--color-muted-foreground)] cursor-pointer"
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
        class="text-xs font-bold uppercase tracking-widest text-[var(--color-muted-foreground)] hover:text-[var(--color-destructive)] transition-colors cursor-pointer px-2 py-1"
      >
        Salir
      </button>
    </div>
  </div>
</header>
