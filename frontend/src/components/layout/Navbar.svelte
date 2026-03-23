<script lang="ts">
  import { push, router } from '../../lib/router.svelte.js';
  import { auth } from '../../stores/auth.svelte.js';
  import { withTransition } from '../../lib/transitions.js';
  import SearchButton from '../search/SearchButton.svelte';
  import { Menu, X } from 'lucide-svelte';
  import { slide } from 'svelte/transition';
  import { expoOut } from 'svelte/easing';

  let container: HTMLElement | undefined = $state();
  let menuOpen = $state(false);

  function navigate(path: string) {
    menuOpen = false;
    withTransition(() => push(path));
  }

  function handleLogout() {
    menuOpen = false;
    auth.logout();
    withTransition(() => push('/'));
  }

  const navLinks = $derived([
    { path: '/products', label: 'Tienda' },
    ...(auth.isAuthenticated ? [{ path: '/profile', label: 'Perfil' }] : []),
    ...(auth.isAdmin
      ? [
          { path: '/admin/products', label: 'Productos' },
          { path: '/admin/users', label: 'Usuarios' },
        ]
      : []),
  ]);

  function isActive(path: string): boolean {
    const loc = router.location;
    if (path === '/products' && loc.startsWith('/products') && !loc.startsWith('/admin'))
      return true;
    if (path === '/admin/products' && loc.startsWith('/admin/products')) return true;
    return loc === path;
  }

  $effect(() => {
    const sentinel = document.createElement('div');
    sentinel.style.cssText =
      'position:absolute;top:50px;left:0;height:1px;width:1px;pointer-events:none;';
    document.body.prepend(sentinel);

    const observer = new IntersectionObserver(([entry]) => {
      container?.classList.toggle('scrolled', !entry.isIntersecting);
    });
    observer.observe(sentinel);

    return () => {
      observer.disconnect();
      sentinel.remove();
    };
  });

  $effect(() => {
    if (!menuOpen) return;

    function handleClickOutside(e: MouseEvent) {
      if (container && !container.contains(e.target as Node)) {
        menuOpen = false;
      }
    }

    // setTimeout evita capturar el mismo clic que abrió el menú
    const id = setTimeout(() => document.addEventListener('click', handleClickOutside), 0);

    return () => {
      clearTimeout(id);
      document.removeEventListener('click', handleClickOutside);
    };
  });
</script>

<header
  id="site-header"
  bind:this={container}
  class="sticky top-0 z-50 border-b transition-all duration-300"
  style="background-color: var(--color-background); border-color: var(--color-border);"
>
  <!-- Barra principal -->
  <div
    id="site-header-bar"
    class="max-w-5xl mx-auto container-padding flex items-center justify-between py-4 sm:py-5 transition-all duration-300"
  >
    <!-- Logo -->
    <button
      onclick={() => navigate('/')}
      class="transition-opacity hover:opacity-70 cursor-pointer flex items-center"
    >
      <img src="/logo.svg" alt="Pear" class="h-7 w-auto" />
    </button>

    <!-- Derecha: búsqueda + hamburguesa -->
    <div class="flex items-center gap-2">
      <SearchButton />
      <button
        onclick={() => (menuOpen = !menuOpen)}
        class="self-stretch flex items-center justify-center px-3 rounded-md transition-all duration-200 cursor-pointer"
        aria-label={menuOpen ? 'Cerrar menú' : 'Abrir menú'}
        style="background: var(--color-secondary); color: var(--color-muted-foreground); border: 1px solid transparent;"
      >
        <div class="relative w-4 h-4">
          <div class="absolute inset-0 flex items-center justify-center transition-all duration-200 {menuOpen ? 'opacity-0 rotate-90' : 'opacity-70 rotate-0'}">
            <Menu size={16} strokeWidth={2.75} />
          </div>
          <div class="absolute inset-0 flex items-center justify-center transition-all duration-200 {menuOpen ? 'opacity-70 rotate-0' : 'opacity-0 -rotate-90'}">
            <X size={16} strokeWidth={2.75} />
          </div>
        </div>
      </button>
    </div>
  </div>

  <!-- Panel desplegable (absoluto, no empuja contenido) -->
  {#if menuOpen}
    <div
      transition:slide={{ duration: 320, easing: expoOut }}
      class="absolute left-0 right-0 border-b overflow-hidden"
      style="top: 100%; background-color: var(--color-background); border-color: var(--color-border);"
    >
      <nav class="max-w-5xl mx-auto container-padding py-2 pb-4">
        {#each navLinks as link, i}
          {@const active = isActive(link.path)}
          <button
            onclick={() => navigate(link.path)}
            class="nav-menu-item w-full text-left px-3 rounded-md transition-colors cursor-pointer hover:bg-accent"
            style="animation-delay: {i * 55}ms;
                   color: {active ? 'var(--color-foreground)' : 'var(--color-muted-foreground)'};
                   font-size: 17px;
                   font-weight: 600;
                   letter-spacing: -0.021em;
                   line-height: 2.6;"
          >
            {link.label}
          </button>
        {/each}

        <div class="pt-3">
          {#if auth.isAuthenticated}
            <button
              onclick={handleLogout}
              class="nav-menu-item w-full text-left px-3 rounded-md transition-colors cursor-pointer hover:bg-accent"
              style="animation-delay: {navLinks.length * 55}ms;
                     color: var(--color-muted-foreground);
                     font-size: 17px;
                     font-weight: 600;
                     letter-spacing: -0.021em;
                     line-height: 2.6;"
            >
              Cerrar sesión
            </button>
          {:else}
            <button
              onclick={() => navigate('/login')}
              class="nav-menu-item w-full text-left px-3 rounded-md transition-colors cursor-pointer hover:bg-accent"
              style="animation-delay: {navLinks.length * 55}ms;
                     color: var(--color-muted-foreground);
                     font-size: 17px;
                     font-weight: 600;
                     letter-spacing: -0.021em;
                     line-height: 2.6;"
            >
              Iniciar sesión
            </button>
          {/if}
        </div>
      </nav>
    </div>
  {/if}
</header>

<style>
  .nav-menu-item {
    animation: navItemIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
  }

  @keyframes navItemIn {
    from {
      opacity: 0;
      transform: translateY(-14px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  :global(#site-header.scrolled) {
    box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  }

  :global(#site-header.scrolled #site-header-bar) {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }

  @media (min-width: 640px) {
    :global(#site-header.scrolled #site-header-bar) {
      padding-top: 0.75rem;
      padding-bottom: 0.75rem;
    }
  }
</style>
