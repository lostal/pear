<script lang="ts">
  import { push, router } from 'svelte-spa-router';
  import { auth } from '../../stores/auth.svelte.js';
  import { withTransition } from '../../lib/transitions.js';

  let container: HTMLElement | undefined = $state();

  function navigate(path: string) {
    withTransition(() => push(path));
  }

  function handleLogout() {
    auth.logout();
    withTransition(() => push('/'));
  }

  const navLinks = $derived(
    auth.isAuthenticated
      ? [
          { path: '/products', label: 'Tienda' },
          { path: '/profile', label: 'Perfil' },
          ...(auth.isAdmin ? [{ path: '/admin/users', label: 'Usuarios' }] : []),
        ]
      : []
  );

  function isActive(path: string): boolean {
    const loc = router.location;
    if (path === '/products' && loc.startsWith('/products')) return true;
    return loc === path;
  }

  $effect(() => {
    function onScroll() {
      container?.classList.toggle('scrolled', window.scrollY > 10);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return () => window.removeEventListener('scroll', onScroll);
  });
</script>

<header
  id="pear-header"
  bind:this={container}
  class="glass-nav sticky top-0 z-40 transition-all duration-300"
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 h-12 flex items-center">
    <!-- Logo zone -->
    <div class="flex-none w-28 sm:w-36">
      <button
        onclick={() => navigate('/')}
        class="font-semibold text-lg tracking-tight hover:opacity-70 transition-opacity cursor-pointer"
      >
        <span style="color: var(--color-apple-blue)">i</span>Pear
      </button>
    </div>

    <!-- Center nav links -->
    <nav class="flex-1 flex justify-center items-center gap-1">
      {#each navLinks as link}
        {@const active = isActive(link.path)}
        <button
          onclick={() => navigate(link.path)}
          class="px-3 py-1 text-sm rounded-full transition-all cursor-pointer
            {active
              ? 'text-[var(--color-foreground)] font-medium'
              : 'text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)]'}"
        >
          {link.label}
        </button>
      {/each}
    </nav>

    <!-- Right actions -->
    <div class="flex-none w-28 sm:w-36 flex justify-end items-center gap-2">
      {#if auth.isAuthenticated}
        <span class="text-xs text-[var(--color-muted-foreground)] hidden sm:block truncate max-w-[80px]">
          {auth.displayName}
        </span>
        <button
          onclick={handleLogout}
          class="text-xs text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)] transition-colors cursor-pointer"
        >
          Salir
        </button>
      {:else}
        <button
          onclick={() => navigate('/login')}
          class="btn-apple text-xs py-1.5 px-4"
        >
          Iniciar sesión
        </button>
      {/if}
    </div>
  </div>
</header>
