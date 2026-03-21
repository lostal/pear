<script lang="ts">
  import Router, { push, router } from 'svelte-spa-router';
  import { wrap } from 'svelte-spa-router/wrap';
  import { auth } from './stores/auth.svelte.js';
  import Navbar from './components/layout/Navbar.svelte';
  import ToastStack from './components/ToastStack.svelte';
  import LoginPage from './pages/LoginPage.svelte';
  import ProductsPage from './pages/ProductsPage.svelte';
  import ProductDetailPage from './pages/ProductDetailPage.svelte';
  import ProfilePage from './pages/ProfilePage.svelte';
  import AdminUsersPage from './pages/AdminUsersPage.svelte';
  import NotFoundPage from './pages/NotFoundPage.svelte';

  // Redirigir a /login si el token expira mientras la app está abierta.
  // router.location es reactivo ($state interno de svelte-spa-router),
  // por lo que el efecto se re-ejecuta tanto al cambiar auth como al navegar.
  $effect(() => {
    if (!auth.isAuthenticated && router.location !== '/login') {
      push('/login');
    }
  });

  const routes = {
    '/': wrap({ component: ProductsPage }),
    '/login': LoginPage,
    '/products': wrap({ component: ProductsPage }),
    '/products/:id': wrap({ component: ProductDetailPage }),
    '/profile': wrap({ component: ProfilePage }),
    '/admin/users': wrap({ component: AdminUsersPage }),
    '*': NotFoundPage,
  };
</script>

{#if auth.isAuthenticated}
  <Navbar />
{/if}

<main>
  <Router {routes} />
</main>

<ToastStack />
