<script lang="ts">
  import { push, router } from '../../lib/router.svelte.js';
  import { auth } from '../../stores/auth.svelte.js';
  import { withTransition } from '../../lib/transitions.js';
  import SearchButton from '../search/SearchButton.svelte';

  let container: HTMLElement | undefined = $state();

  function navigate(path: string) {
    withTransition(() => push(path));
  }

  const navLinks = $derived([
    { path: '/products', label: 'Tienda' },
    ...(auth.isAuthenticated ? [{ path: '/profile', label: 'Perfil' }] : []),
    ...(auth.isAdmin ? [{ path: '/admin/users', label: 'Usuarios' }] : []),
  ]);

  function isActive(path: string): boolean {
    const loc = router.location;
    if (path === '/products' && loc.startsWith('/products')) return true;
    return loc === path;
  }

  $effect(() => {
    function onScroll() {
      if (!container) return;
      container.classList.toggle('scrolled', window.scrollY > 50);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return () => window.removeEventListener('scroll', onScroll);
  });
</script>

<header
  id="site-header"
  bind:this={container}
  class="sticky top-0 z-50 border-b transition-all duration-300"
  style="background-color: color-mix(in srgb, var(--color-background) 80%, transparent);
         backdrop-filter: saturate(180%) blur(20px);
         -webkit-backdrop-filter: saturate(180%) blur(20px);
         border-color: var(--color-border);"
>
  <div class="max-w-5xl mx-auto container-padding grid items-center py-4 sm:py-5 transition-all duration-300" style="grid-template-columns: 1fr auto 1fr;">
    <!-- Logo -->
    <button
      onclick={() => navigate('/')}
      class="transition-opacity hover:opacity-70 cursor-pointer flex items-center justify-self-start"
    >
      <img src="/logo.svg" alt="Pear" class="h-7 w-auto" />
    </button>

    <!-- Nav links (siempre centrado) -->
    <nav class="flex items-center gap-1">
      {#each navLinks as link}
        {@const active = isActive(link.path)}
        <button
          onclick={() => navigate(link.path)}
          class="px-3 py-1.5 text-sm rounded-md transition-colors cursor-pointer
            {active
              ? 'font-black'
              : 'hover:bg-accent'}"
          style="color: {active ? 'var(--color-foreground)' : 'var(--color-muted-foreground)'};"
        >
          {link.label}
        </button>
      {/each}
    </nav>

    <!-- Derecha: búsqueda -->
    <div class="flex items-center justify-self-end">
      <SearchButton />
    </div>
  </div>
</header>

<style>
  :global(#site-header.scrolled) {
    box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  }

  :global(#site-header.scrolled > div) {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }

  @media (min-width: 640px) {
    :global(#site-header.scrolled > div) {
      padding-top: 0.75rem;
      padding-bottom: 0.75rem;
    }
  }
</style>
