<script lang="ts">
  import Router, { push, router } from 'svelte-spa-router';
  import { wrap } from 'svelte-spa-router/wrap';
  import { auth } from './stores/auth.svelte.js';
  import Navbar from './components/layout/Navbar.svelte';
  import ToastStack from './components/ToastStack.svelte';
  import LandingPage from './pages/LandingPage.svelte';
  import LoginPage from './pages/LoginPage.svelte';
  import ProductsPage from './pages/ProductsPage.svelte';
  import ProductDetailPage from './pages/ProductDetailPage.svelte';
  import ProfilePage from './pages/ProfilePage.svelte';
  import AdminUsersPage from './pages/AdminUsersPage.svelte';
  import NotFoundPage from './pages/NotFoundPage.svelte';

  const publicRoutes = ['/', '/login'];

  $effect(() => {
    if (!auth.isAuthenticated && !publicRoutes.includes(router.location)) {
      push('/');
    }
  });

  const routes = {
    '/': LandingPage,
    '/login': LoginPage,
    '/products': wrap({ component: ProductsPage }),
    '/products/:id': wrap({ component: ProductDetailPage }),
    '/profile': wrap({ component: ProfilePage }),
    '/admin/users': wrap({ component: AdminUsersPage }),
    '*': NotFoundPage,
  };
</script>

<Navbar />

<main>
  <Router {routes} />
</main>

<ToastStack />
