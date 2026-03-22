<script lang="ts">
  import Router from './lib/Router.svelte';
  import { push, router } from './lib/router.svelte.js';
  import { auth } from './stores/auth.svelte.js';
  import Navbar from './components/layout/Navbar.svelte';
  import { Toaster } from 'svelte-sonner';
  import SearchDialog from './components/search/SearchDialog.svelte';
  import LandingPage from './pages/LandingPage.svelte';
  import LoginPage from './pages/LoginPage.svelte';
  import ProductsPage from './pages/ProductsPage.svelte';
  import ProductDetailPage from './pages/ProductDetailPage.svelte';
  import ProfilePage from './pages/ProfilePage.svelte';
  import AdminUsersPage from './pages/AdminUsersPage.svelte';
  import AdminProductsPage from './pages/AdminProductsPage.svelte';
  import AdminProductEditPage from './pages/AdminProductEditPage.svelte';
  import NotFoundPage from './pages/NotFoundPage.svelte';

  const protectedRoutes = ['/profile', '/admin/users', '/admin/products'];

  $effect(() => {
    if (!auth.isAuthenticated && protectedRoutes.some((r) => router.location.startsWith(r))) {
      push('/');
    }
  });

  const routes = {
    '/': LandingPage,
    '/login': LoginPage,
    '/products': ProductsPage,
    '/products/:id': ProductDetailPage,
    '/profile': ProfilePage,
    '/admin/users': AdminUsersPage,
    '/admin/products': AdminProductsPage,
    '/admin/products/:id': AdminProductEditPage,
    '*': NotFoundPage,
  };
</script>

<Navbar />

<main>
  <Router {routes} />
</main>

<Toaster richColors position="bottom-right" />
<SearchDialog />
