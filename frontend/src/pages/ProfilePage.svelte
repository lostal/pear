<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { auth } from '../stores/auth.svelte.js';
  import Button from '../components/ui/Button.svelte';
  import PageLayout from '../components/layout/PageLayout.svelte';

  $effect(() => {
    if (!auth.isAuthenticated) push('/');
  });

  function handleLogout() {
    auth.logout();
    push('/');
  }
</script>

<PageLayout narrow>
  {#if auth.user}
    <!-- Avatar + info -->
    <div class="pb-8 mb-8 border-b flex items-center gap-5" style="border-color: var(--color-border);">
      <div
        class="h-16 w-16 rounded-full flex items-center justify-center text-2xl font-black border"
        style="background-color: var(--color-secondary); color: var(--color-foreground); border-color: var(--color-border);"
      >
        {auth.user.username[0].toUpperCase()}
      </div>
      <div>
        <h2 class="text-2xl font-black">{auth.user.username}</h2>
        <p class="text-sm mt-0.5" style="color: var(--color-muted-foreground); text-transform: capitalize;">
          {auth.user.role}
        </p>
      </div>
    </div>

    <!-- Logout -->
    <Button variant="destructive" onclick={handleLogout} class="w-full sm:w-auto">
      Cerrar sesión
    </Button>
  {/if}
</PageLayout>
