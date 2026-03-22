<script lang="ts">
  import Router from './lib/Router.svelte';
  import { push, router } from './lib/router.svelte.js';
  import { auth } from './stores/auth.svelte.js';
  import Navbar from './components/layout/Navbar.svelte';
  import { Toaster } from 'svelte-sonner';
  import SearchDialog from './components/search/SearchDialog.svelte';
  import { preloadRoutes } from './lib/routeCache.js';

  const protectedRoutes = ['/profile', '/admin/users', '/admin/products'];

  const pageTitles: Record<string, string> = {
    '/': 'Pear',
    '/login': 'Iniciar sesión — Pear',
    '/products': 'Tienda — Pear',
    '/profile': 'Perfil — Pear',
    '/admin/products': 'Admin · Productos — Pear',
    '/admin/users': 'Admin · Usuarios — Pear',
  };

  $effect(() => {
    document.title = pageTitles[router.location] ?? 'Pear';
  });

  $effect(() => {
    if (!auth.isAuthenticated && protectedRoutes.some((r) => router.location.startsWith(r))) {
      push('/');
    }
  });

  const routes = {
    '/': () => import('./pages/LandingPage.svelte'),
    '/login': () => import('./pages/LoginPage.svelte'),
    '/products': () => import('./pages/ProductsPage.svelte'),
    '/products/:id': () => import('./pages/ProductDetailPage.svelte'),
    '/profile': () => import('./pages/ProfilePage.svelte'),
    '/admin/users': () => import('./pages/AdminUsersPage.svelte'),
    '/admin/products': () => import('./pages/AdminProductsPage.svelte'),
    '/admin/products/:id': () => import('./pages/AdminProductEditPage.svelte'),
    '*': () => import('./pages/NotFoundPage.svelte'),
  };

  // Precarga en la caché compartida para que las view transitions sean síncronas
  $effect(() => {
    preloadRoutes(Object.values(routes));
  });
</script>

<Navbar />

<main>
  <Router {routes} />
</main>

<Toaster richColors position="bottom-right" />
<SearchDialog />
